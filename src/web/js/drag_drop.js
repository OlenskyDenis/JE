/**
 * Drag & Drop Module implementing Three-Zone Hit Testing, Cycle Validation,
 * and Non-Destructive Sidebar Header Catalog Drag-and-Drop (Feature 002).
 */

const DragDropHandler = {
    draggedNodeId: null,
    draggedSidebarHeader: null,
    activeDropTarget: null,
    activeDropZone: null,

    init(treeViewEl, onMoveNodeCallback, onAddHeaderNodeCallback, showToastCallback) {
        this.treeViewEl = treeViewEl;
        this.onMoveNode = onMoveNodeCallback;
        this.onAddHeaderNode = onAddHeaderNodeCallback;
        this.showToast = showToastCallback;

        this.bindEvents();
    },

    bindEvents() {
        this.treeViewEl.addEventListener('dragstart', (e) => this.handleDragStart(e));
        this.treeViewEl.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.treeViewEl.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.treeViewEl.addEventListener('drop', (e) => this.handleDrop(e));
        this.treeViewEl.addEventListener('dragend', (e) => this.handleDragEnd(e));
    },

    bindSidebarItem(sidebarItemEl) {
        sidebarItemEl.setAttribute('draggable', 'true');
        sidebarItemEl.addEventListener('dragstart', (e) => {
            const headerLabel = sidebarItemEl.dataset.headerLabel;
            this.draggedSidebarHeader = headerLabel;
            this.draggedNodeId = null;
            e.dataTransfer.setData('text/plain', headerLabel);
            e.dataTransfer.setData('source', 'sidebar_catalog');
            e.dataTransfer.effectAllowed = 'copy';
        });
        sidebarItemEl.addEventListener('dragend', () => {
            this.draggedSidebarHeader = null;
            this.clearDropHighlights();
        });
    },

    handleDragStart(e) {
        const nodeContent = e.target.closest('.tree-node-content');
        if (!nodeContent) return;

        this.draggedSidebarHeader = null;
        this.draggedNodeId = nodeContent.dataset.id;
        nodeContent.classList.add('dragging');
        e.dataTransfer.setData('text/plain', this.draggedNodeId);
        e.dataTransfer.setData('source', 'tree_node');
        e.dataTransfer.effectAllowed = 'move';
    },

    handleDragOver(e) {
        e.preventDefault();
        const targetContent = e.target.closest('.tree-node-content');
        
        // Handle drop onto empty canvas when dragging from sidebar
        if (!targetContent) {
            if (this.draggedSidebarHeader) {
                e.dataTransfer.dropEffect = 'copy';
            }
            return;
        }

        const targetId = targetContent.dataset.id;

        if (this.draggedNodeId) {
            if (targetId === this.draggedNodeId) {
                e.dataTransfer.dropEffect = 'none';
                return;
            }

            // Check if target is inside dragged node (cycle prevention)
            const draggedNodeWrapper = this.treeViewEl.querySelector(`.tree-node[data-id="${this.draggedNodeId}"]`);
            if (draggedNodeWrapper && draggedNodeWrapper.contains(targetContent)) {
                e.dataTransfer.dropEffect = 'none';
                targetContent.classList.add('drop-prohibited');
                document.body.classList.add('drag-prohibited');
                return;
            } else {
                targetContent.classList.remove('drop-prohibited');
                document.body.classList.remove('drag-prohibited');
            }
        }

        // Calculate Three-Zone Hit Target
        const rect = targetContent.getBoundingClientRect();
        const relativeY = (e.clientY - rect.top) / rect.height;
        const isContainer = targetContent.closest('.tree-node').dataset.isContainer === 'true';

        let zone = 'NEST_CHILD';
        if (relativeY < 0.25) {
            zone = 'BEFORE_SIBLING';
        } else if (relativeY > 0.75) {
            zone = 'AFTER_SIBLING';
        } else if (!isContainer) {
            zone = relativeY < 0.5 ? 'BEFORE_SIBLING' : 'AFTER_SIBLING';
        }

        this.clearDropHighlights();
        this.activeDropTarget = targetContent;
        this.activeDropZone = zone;

        if (zone === 'BEFORE_SIBLING') {
            targetContent.classList.add('drop-zone-before');
        } else if (zone === 'AFTER_SIBLING') {
            targetContent.classList.add('drop-zone-after');
        } else if (zone === 'NEST_CHILD') {
            targetContent.classList.add('drop-zone-inside');
        }
        e.dataTransfer.dropEffect = this.draggedSidebarHeader ? 'copy' : 'move';
    },

    handleDragLeave(e) {
        const targetContent = e.target.closest('.tree-node-content');
        if (targetContent) {
            targetContent.classList.remove('drop-zone-before', 'drop-zone-after', 'drop-zone-inside', 'drop-prohibited');
        }
        document.body.classList.remove('drag-prohibited');
    },

    async handleDrop(e) {
        e.preventDefault();
        const source = e.dataTransfer.getData('source');
        const targetContent = e.target.closest('.tree-node-content');

        // Case 1: Drop sidebar catalog header into canvas (non-destructive)
        if (source === 'sidebar_catalog' || this.draggedSidebarHeader) {
            const headerLabel = this.draggedSidebarHeader || e.dataTransfer.getData('text/plain');
            if (!headerLabel) return;

            const parentId = targetContent ? targetContent.dataset.id : null;
            this.clearDropHighlights();
            if (this.onAddHeaderNode) {
                await this.onAddHeaderNode(parentId, headerLabel);
            }
            this.draggedSidebarHeader = null;
            return;
        }

        // Case 2: Tree node reordering / moving
        if (!targetContent || !this.draggedNodeId) return;

        const targetId = targetContent.dataset.id;
        const zone = this.activeDropZone;

        this.clearDropHighlights();

        const draggedNodeWrapper = this.treeViewEl.querySelector(`.tree-node[data-id="${this.draggedNodeId}"]`);
        if (targetId === this.draggedNodeId || (draggedNodeWrapper && draggedNodeWrapper.contains(targetContent))) {
            this.showToast('Invalid Operation: Cannot move a node into itself or its own descendant.', 'warning');
            return;
        }

        if (this.onMoveNode && zone) {
            await this.onMoveNode(this.draggedNodeId, targetId, zone);
        }
    },

    handleDragEnd(e) {
        const dragging = this.treeViewEl.querySelector('.dragging');
        if (dragging) {
            dragging.classList.remove('dragging');
        }
        this.clearDropHighlights();
        document.body.classList.remove('drag-prohibited');
        this.draggedNodeId = null;
        this.draggedSidebarHeader = null;
        this.activeDropTarget = null;
        this.activeDropZone = null;
    },

    clearDropHighlights() {
        const highlighted = this.treeViewEl.querySelectorAll('.drop-zone-before, .drop-zone-after, .drop-zone-inside, .drop-prohibited');
        highlighted.forEach(el => el.classList.remove('drop-zone-before', 'drop-zone-after', 'drop-zone-inside', 'drop-prohibited'));
    }
};
