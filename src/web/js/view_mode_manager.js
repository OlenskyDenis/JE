/**
 * View Mode Manager (Feature 027, 028, 030, 033)
 * Coordinates View Mode Selection (Tree, Matrix, Unique Levels), Canvas Rendering, and Double-Click Event Routing.
 */

const ViewModeManager = {
    app: null,
    currentViewMode: 'tree',

    init(app) {
        this.app = app;
        this.bindDOM();
        this.bindEvents();

        const savedView = localStorage.getItem('je_workspace_view_mode');
        this.currentViewMode = (savedView === 'matrix' || savedView === 'unique_levels') ? savedView : 'tree';
        this.switchViewMode(this.currentViewMode);
    },

    bindDOM() {
        this.btnViewTree = document.getElementById('btnViewTree');
        this.btnViewMatrix = document.getElementById('btnViewMatrix');
        this.btnViewUniqueLevels = document.getElementById('btnViewUniqueLevels');
        this.treeViewEl = document.getElementById('treeView');
        this.excelBlockViewEl = document.getElementById('excelBlockView');
        this.uniqueLevelViewEl = document.getElementById('uniqueLevelView');
    },

    bindEvents() {
        if (this.btnViewTree) this.btnViewTree.addEventListener('click', () => this.switchViewMode('tree'));
        if (this.btnViewMatrix) this.btnViewMatrix.addEventListener('click', () => this.switchViewMode('matrix'));
        if (this.btnViewUniqueLevels) this.btnViewUniqueLevels.addEventListener('click', () => this.switchViewMode('unique_levels'));

        // Tree click / double click
        if (this.treeViewEl) {
            this.treeViewEl.addEventListener('click', (e) => {
                const btnAddCanvas = e.target.closest('#btnAddRootCanvas') || e.target.closest('.btn-add-root-canvas');
                if (btnAddCanvas) {
                    e.stopPropagation();
                    const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
                    if (window.ModalManager) ModalManager.openAddModal(null, t("modal_create_title"));
                    return;
                }
                const toggleBtn = e.target.closest('.node-toggle');
                if (toggleBtn) {
                    e.stopPropagation();
                    const nodeId = toggleBtn.getAttribute('data-id');
                    if (this.app) this.app.toggleNodeCollapse(nodeId);
                    return;
                }
                const btnAdd = e.target.closest('.action-btn.add-child');
                if (btnAdd) {
                    e.stopPropagation();
                    const parentId = btnAdd.getAttribute('data-id');
                    const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
                    if (window.ModalManager) ModalManager.openAddModal(parentId, t("modal_create_child_title"));
                    return;
                }
                const btnRename = e.target.closest('.action-btn.rename-node');
                if (btnRename) {
                    e.stopPropagation();
                    const nodeId = btnRename.getAttribute('data-id');
                    const nodeWrapper = btnRename.closest('.tree-node');
                    const titleEl = nodeWrapper ? nodeWrapper.querySelector('.node-title') : null;
                    const name = titleEl ? titleEl.textContent.trim() : '';
                    const type = nodeWrapper ? nodeWrapper.dataset.dataType : 'Text';
                    const isFolder = nodeWrapper ? (nodeWrapper.dataset.isFolder === 'true') : false;
                    if (window.ModalManager) ModalManager.openEditModal(nodeId, name, type, isFolder);
                    return;
                }
                const btnDel = e.target.closest('.action-btn.delete');
                if (btnDel) {
                    e.stopPropagation();
                    const nodeId = btnDel.getAttribute('data-id');
                    if (this.app) this.app.handleNodeDelete(nodeId);
                    return;
                }
            });

            this.treeViewEl.addEventListener('dblclick', (e) => {
                const nodeItem = e.target.closest('.tree-node');
                if (nodeItem && !e.target.closest('.action-btn') && !e.target.closest('.node-toggle')) {
                    const nodeId = nodeItem.dataset.id;
                    const titleEl = nodeItem.querySelector('.node-title');
                    const name = titleEl ? titleEl.textContent.trim() : '';
                    const type = nodeItem.dataset.dataType || 'Text';
                    const isFolder = nodeItem.dataset.isFolder === 'true';
                    if (window.ModalManager) ModalManager.openEditModal(nodeId, name, type, isFolder);
                }
            });
        }

        // Matrix double click
        if (this.excelBlockViewEl) {
            this.excelBlockViewEl.addEventListener('dblclick', (e) => {
                const cell = e.target.closest('.matrix-cell');
                if (cell) {
                    const nodeId = cell.getAttribute('data-node-id');
                    const name = cell.getAttribute('data-node-name');
                    const type = cell.getAttribute('data-data-type') || 'Text';
                    const isFolder = cell.getAttribute('data-is-folder') === 'true';
                    if (window.ModalManager) ModalManager.openEditModal(nodeId, name, type, isFolder);
                }
            });
        }

        // Unique level double click
        if (this.uniqueLevelViewEl) {
            this.uniqueLevelViewEl.addEventListener('dblclick', (e) => {
                const chip = e.target.closest('.level-header-chip');
                if (chip) {
                    const nodeId = chip.getAttribute('data-node-id');
                    const name = chip.getAttribute('data-node-name');
                    const type = chip.getAttribute('data-data-type') || 'Text';
                    const isFolder = chip.getAttribute('data-is-folder') === 'true';
                    const nodeIdsStr = chip.getAttribute('data-node-ids') || nodeId;
                    const batchNodeIds = nodeIdsStr.split(',').filter(Boolean);
                    const batchCount = parseInt(chip.getAttribute('data-count') || '1', 10);
                    if (window.ModalManager) ModalManager.openEditModal(nodeId, name, type, isFolder, batchCount, batchNodeIds);
                }
            });
        }
    },

    switchViewMode(mode) {
        this.currentViewMode = mode;
        localStorage.setItem('je_workspace_view_mode', mode);

        if (this.btnViewTree) this.btnViewTree.classList.toggle('active', mode === 'tree');
        if (this.btnViewMatrix) this.btnViewMatrix.classList.toggle('active', mode === 'matrix');
        if (this.btnViewUniqueLevels) this.btnViewUniqueLevels.classList.toggle('active', mode === 'unique_levels');
        if (this.treeViewEl) this.treeViewEl.classList.toggle('hidden', mode !== 'tree');
        if (this.excelBlockViewEl) this.excelBlockViewEl.classList.toggle('hidden', mode !== 'matrix');
        if (this.uniqueLevelViewEl) this.uniqueLevelViewEl.classList.toggle('hidden', mode !== 'unique_levels');

        if (this.app) this.renderCurrentView(this.app.currentRoots);
    },

    renderCurrentView(roots) {
        const collapsedSet = (this.app && this.app.collapsedNodeIds) ? this.app.collapsedNodeIds : new Set();
        if (this.currentViewMode === 'tree') {
            if (window.TreeRenderer && this.treeViewEl) {
                TreeRenderer.renderTree(roots, this.treeViewEl, collapsedSet);
            }
        } else if (this.currentViewMode === 'matrix') {
            if (window.ExcelBlockRenderer && this.excelBlockViewEl) {
                ExcelBlockRenderer.renderMatrix(roots, this.excelBlockViewEl);
            }
        } else if (this.currentViewMode === 'unique_levels') {
            if (window.UniqueLevelRenderer && this.uniqueLevelViewEl) {
                UniqueLevelRenderer.renderUniqueLevels(roots, this.uniqueLevelViewEl);
            }
        }
    }
};

window.ViewModeManager = ViewModeManager;
