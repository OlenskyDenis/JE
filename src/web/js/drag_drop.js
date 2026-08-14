/**
 * Drag & Drop Module implementing Three-Zone Hit Testing, Cycle Validation,
 * and Unified Interaction Handling for workspace reordering and Excel Header Catalog drops.
 */

const DragDropHandler = {
    activeDragPayload: null, // Unified payload: { isNew: boolean, id?: string, label?: string, isContainer?: boolean }
    activeDropTarget: null,
    activeDropZone: null,

    init(treeViewEl, onDropPayloadCallback, showToastCallback) {
        this.treeViewEl = treeViewEl;
        this.onDropPayload = onDropPayloadCallback;
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
            this.activeDragPayload = { isNew: true, label: headerLabel };
            e.dataTransfer.setData('application/json', JSON.stringify(this.activeDragPayload));
            e.dataTransfer.setData('text/plain', headerLabel);
            e.dataTransfer.setData('source', 'sidebar_catalog');
            e.dataTransfer.effectAllowed = 'copy';
        });
        sidebarItemEl.addEventListener('dragend', () => {
            this.handleDragEnd();
        });
    },

    handleDragStart(e) {
        const nodeContent = e.target.closest('.tree-node-content');
        if (!nodeContent) return;

        const nodeId = nodeContent.dataset.id;
        this.activeDragPayload = { isNew: false, id: nodeId };
        nodeContent.classList.add('dragging');

        e.dataTransfer.setData('application/json', JSON.stringify(this.activeDragPayload));
        e.dataTransfer.setData('text/plain', nodeId);
        e.dataTransfer.setData('source', 'tree_node');
        e.dataTransfer.effectAllowed = 'move';
    },

    getDragPayload(e) {
        if (this.activeDragPayload) {
            return this.activeDragPayload;
        }
        try {
            const jsonStr = e.dataTransfer.getData('application/json');
            if (jsonStr) {
                return JSON.parse(jsonStr);
            }
        } catch (err) {
            // Fallback for non-JSON transfers
        }
        const source = e.dataTransfer.getData('source');
        if (source === 'sidebar_catalog') {
            const label = e.dataTransfer.getData('text/plain');
            return { isNew: true, label: label };
        } else if (source === 'tree_node') {
            const id = e.dataTransfer.getData('text/plain');
            return { isNew: false, id: id };
        }
        return null;
    },

    handleDragOver(e) {
        e.preventDefault();
        const payload = this.getDragPayload(e);
        const targetContent = e.target.closest('.tree-node-content');

        // Handle drop onto empty workspace canvas
        if (!targetContent) {
            if (payload && payload.isNew) {
                e.dataTransfer.dropEffect = 'copy';
            }
            return;
        }

        const targetId = targetContent.dataset.id;

        // Cycle check only applies when reordering existing workspace nodes
        if (payload && !payload.isNew && payload.id) {
            if (targetId === payload.id) {
                e.dataTransfer.dropEffect = 'none';
                return;
            }

            const draggedNodeWrapper = this.treeViewEl.querySelector(`.tree-node[data-id="${payload.id}"]`);
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

        // Three-Zone Hit Testing (Unified Y-coordinate positioning calculation)
        const rect = targetContent.getBoundingClientRect();
        const relativeY = (e.clientY - rect.top) / rect.height;

        let zone = 'NEST_CHILD';
        if (relativeY < 0.25) {
            zone = 'BEFORE_SIBLING';
        } else if (relativeY > 0.75) {
            zone = 'AFTER_SIBLING';
        } else {
            zone = 'NEST_CHILD';
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
        e.dataTransfer.dropEffect = (payload && payload.isNew) ? 'copy' : 'move';
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
        const payload = this.getDragPayload(e);
        if (!payload) return;

        const targetContent = e.target.closest('.tree-node-content');
        const targetId = targetContent ? targetContent.dataset.id : null;
        const zone = this.activeDropZone;

        this.clearDropHighlights();

        if (!payload.isNew && payload.id && targetId) {
            const draggedNodeWrapper = this.treeViewEl.querySelector(`.tree-node[data-id="${payload.id}"]`);
            if (targetId === payload.id || (draggedNodeWrapper && draggedNodeWrapper.contains(targetContent))) {
                if (this.showToast) {
                    this.showToast('Invalid Operation: Cannot move a node into itself or its own descendant.', 'warning');
                }
                this.handleDragEnd();
                return;
            }
        }

        if (this.onDropPayload) {
            await this.onDropPayload(payload, targetId, zone);
        }

        this.handleDragEnd();
    },

    handleDragEnd() {
        const dragging = this.treeViewEl.querySelector('.dragging');
        if (dragging) {
            dragging.classList.remove('dragging');
        }
        this.clearDropHighlights();
        document.body.classList.remove('drag-prohibited');
        this.activeDragPayload = null;
        this.activeDropTarget = null;
        this.activeDropZone = null;
    },

    clearDropHighlights() {
        const highlighted = this.treeViewEl.querySelectorAll('.drop-zone-before, .drop-zone-after, .drop-zone-inside, .drop-prohibited');
        highlighted.forEach(el => el.classList.remove('drop-zone-before', 'drop-zone-after', 'drop-zone-inside', 'drop-prohibited'));
    }
};
