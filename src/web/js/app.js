/**
 * Main Application Module connecting Eel RPC backend with HTML5 Frontend.
 * Includes Excel Header Catalog Sidebar, Sheet Manager (Feature 002),
 * Native OS File Dialogs (Feature 003), and Dynamic Folder Collapse/Expand (Feature 011).
 */

document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

const App = {
    activeParentIdForModal: null,
    activeNodeIdForEdit: null,
    modalMode: 'create',
    currentFileName: null,
    currentSheetName: null,
    catalogSheetName: null,
    cachedAllHeaders: {},
    cachedAllHeadersMeta: {},
    pendingAction: null,
    isDirty: false,
    currentTemplatePath: null,
    currentRawHeaders: [],
    currentRawHeadersMeta: [],
    collapsedNodeIds: new Set(),
    currentRoots: [],

    async init() {
        this.collapsedNodeIds = new Set();
        this.currentRoots = [];
        this.cachedAllHeaders = {};
        this.cachedAllHeadersMeta = {};
        this.currentRawHeadersMeta = [];
        this.isDirty = false;
        this.currentTemplatePath = null;
        this.pendingAction = null;
        this.modalMode = 'create';
        this.activeNodeIdForEdit = null;
        this.bindDOM();
        this.bindEvents();

        if (window.I18n) {
            I18n.init();
            I18n.onLanguageChanged(() => {
                this.updateTemplateBadge(this.currentTemplatePath);
                this.updateUI(this.currentRoots);
                this.filterAndRenderSidebar();
                this.updateSheetSelectorsLabels();
            });
        }

        DragDropHandler.init(
            document.getElementById('treeView'),
            (payload, targetId, zone) => this.handleDropPayload(payload, targetId, zone),
            (msg, type) => this.showToast(msg, type)
        );

        await this.refreshWorkspace();
    },

    bindDOM() {
        this.treeViewEl = document.getElementById('treeView');
        this.pathListEl = document.getElementById('pathList');
        this.nodeCountBadge = document.getElementById('nodeCountBadge');
        this.templateStatusBadge = document.getElementById('templateStatusBadge');
        this.toastContainer = document.getElementById('toastContainer');
        this.nodeModal = document.getElementById('nodeModal');
        this.modalTitle = document.getElementById('modalTitle');
        this.inputNodeName = document.getElementById('inputNodeName');
        this.groupNodeType = document.getElementById('groupNodeType');
        this.selectNodeType = document.getElementById('selectNodeType');
        this.folderTypeHint = document.getElementById('folderTypeHint');
        this.btnModalSubmit = document.getElementById('btnModalSubmit');

        // Toolbar Collapse / Expand & Add Root buttons (Feature 011 & 025)
        this.btnExpandAll = document.getElementById('btnExpandAll');
        this.btnCollapseAll = document.getElementById('btnCollapseAll');
        this.btnAddRootHeader = document.getElementById('btnAddRootHeader');

        // Language switcher buttons (Feature 023)
        this.langBtnUk = document.getElementById('langBtnUk');
        this.langBtnEn = document.getElementById('langBtnEn');

        // Unified Sidebar & Tabs (Feature 013 & 015)
        this.unifiedSidebar = document.getElementById('unifiedSidebar');
        this.sidebarResizer = document.getElementById('sidebarResizer');
        this.tabBtnCatalog = document.getElementById('tabBtnCatalog');
        this.tabBtnPaths = document.getElementById('tabBtnPaths');
        this.tabContentCatalog = document.getElementById('tabContentCatalog');
        this.tabContentPaths = document.getElementById('tabContentPaths');

        // Sidebar DOM elements (Feature 002 & 015)
        this.activeSheetSelector = document.getElementById('activeSheetSelector');
        this.catalogSheetSelector = document.getElementById('catalogSheetSelector');
        this.sidebarSearch = document.getElementById('sidebarSearch');
        this.sidebarHeaderList = document.getElementById('sidebarHeaderList');
        this.sidebarEmptyState = document.getElementById('sidebarEmptyState');
        this.headerCountBadge = document.getElementById('headerCountBadge');
        this.pathCountBadge = document.getElementById('pathCountBadge');

        // Unsaved Changes Modal (Feature 015 & 016)
        this.unsavedModal = document.getElementById('unsavedModal');
        this.unsavedModalMessage = document.getElementById('unsavedModalMessage');
        this.unsavedModalClose = document.getElementById('unsavedModalClose');
        this.btnUnsavedCancel = document.getElementById('btnUnsavedCancel');
        this.btnUnsavedDiscard = document.getElementById('btnUnsavedDiscard');
        this.btnUnsavedSave = document.getElementById('btnUnsavedSave');
    },

    updateTemplateBadge(path) {
        this.currentTemplatePath = path || null;
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        if (this.templateStatusBadge) {
            if (this.currentTemplatePath) {
                const base = this.currentTemplatePath.split(/[/\\]/).pop();
                this.templateStatusBadge.textContent = `${t('template_prefix')}: ${base} (Synced)`;
                this.templateStatusBadge.title = `${t('template_status_title')}: ${this.currentTemplatePath}`;
            } else {
                this.templateStatusBadge.textContent = `${t('template_prefix')}: ${t('template_none')}`;
                this.templateStatusBadge.title = t('template_status_title');
            }
        }
    },

    bindEvents() {
        this.bindTabs();
        this.bindResizer();

        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);

        // Language Switcher (Feature 023)
        if (this.langBtnUk) {
            this.langBtnUk.addEventListener('click', () => {
                if (window.I18n) I18n.setLanguage('uk');
            });
        }
        if (this.langBtnEn) {
            this.langBtnEn.addEventListener('click', () => {
                if (window.I18n) I18n.setLanguage('en');
            });
        }

        const btnCreateRootEmpty = document.getElementById('btnCreateRootEmpty');
        if (btnCreateRootEmpty) {
            btnCreateRootEmpty.addEventListener('click', () => this.openAddModal(null, t("modal_create_title")));
        }
        if (this.btnAddRootHeader) {
            this.btnAddRootHeader.addEventListener('click', () => this.openAddModal(null, t("modal_create_title")));
        }
        document.getElementById('btnRefresh').addEventListener('click', () => this.refreshWorkspace());

        // Feature 011: Global Toolbar Expand All / Collapse All
        if (this.btnExpandAll) {
            this.btnExpandAll.addEventListener('click', () => this.expandAll());
        }
        if (this.btnCollapseAll) {
            this.btnCollapseAll.addEventListener('click', () => this.collapseAll());
        }

        // Helper: Native OS Open File Dialog for Excel Import
        this.promptOpenAndImportFile = async () => {
            try {
                const dialogRes = await eel.open_file_dialog()();
                if (dialogRes && dialogRes.success && !dialogRes.cancelled && dialogRes.file_path) {
                    await this.handleImportExcelFile(dialogRes.file_path);
                }
            } catch (err) {
                this.showToast("RPC Error opening file dialog: " + err, "error");
            }
        };

        // Feature 003 & 018: Native OS Open File Dialog for Excel Import with Dirty State Protection
        document.getElementById('btnImportExcel').addEventListener('click', async () => {
            if (this.isDirty) {
                this.pendingAction = { type: 'import_file' };
                if (this.currentTemplatePath) {
                    const base = this.currentTemplatePath.split(/[/\\]/).pop();
                    this.unsavedModalMessage.innerHTML = t('unsaved_msg_import_update', { template: this.escapeHtml(base) });
                    this.btnUnsavedSave.textContent = t("unsaved_btn_update_import");
                } else {
                    this.unsavedModalMessage.innerHTML = t('unsaved_msg_import_save');
                    this.btnUnsavedSave.textContent = t("unsaved_btn_save_import");
                }
                this.btnUnsavedDiscard.textContent = t("unsaved_btn_discard_import");
                this.unsavedModal.classList.remove('hidden');
            } else {
                await this.promptOpenAndImportFile();
            }
        });

        // Feature 003, 014 & 016: Native OS Save File Dialog for Template Export with multi-sheet sync
        document.getElementById('btnExportExcel').addEventListener('click', async () => {
            try {
                let defaultName = "Шаблон_reorganized_headers_export.xlsx";
                if (this.currentFileName) {
                    defaultName = `Шаблон_${this.currentFileName}`;
                }
                const dialogRes = await eel.save_file_dialog(defaultName)();
                if (dialogRes && dialogRes.success && !dialogRes.cancelled && dialogRes.file_path) {
                    const res = await eel.save_template_sync(dialogRes.file_path)();
                    if (res.success) {
                        this.isDirty = false;
                        this.updateTemplateBadge(res.template_path);
                        this.showToast(t('toast_template_exported', { template: res.template_path.split(/[/\\]/).pop() }), "success");
                    } else {
                        this.showToast(res.error || t("toast_template_failed"), "error");
                    }
                }
            } catch (err) {
                this.showToast("RPC Error opening save dialog: " + err, "error");
            }
        });

        // Feature 015 & 016: Active Workspace Sheet Change with Template Sync Prompt
        this.activeSheetSelector.addEventListener('change', (e) => {
            const selectedSheet = e.target.value;
            if (!selectedSheet || selectedSheet === this.currentSheetName) return;

            if (this.isDirty) {
                this.pendingAction = { type: 'switch_sheet', targetSheet: selectedSheet };
                if (this.currentTemplatePath) {
                    const base = this.currentTemplatePath.split(/[/\\]/).pop();
                    this.unsavedModalMessage.innerHTML = t('unsaved_msg_switch_update', { sheet: this.escapeHtml(this.currentSheetName || 'Active Sheet'), template: this.escapeHtml(base), target: this.escapeHtml(selectedSheet) });
                    this.btnUnsavedSave.textContent = t("unsaved_btn_update_switch");
                } else {
                    this.unsavedModalMessage.innerHTML = t('unsaved_msg_switch_save', { sheet: this.escapeHtml(this.currentSheetName || 'Active Sheet'), target: this.escapeHtml(selectedSheet) });
                    this.btnUnsavedSave.textContent = t("unsaved_btn_save_switch");
                }
                this.btnUnsavedDiscard.textContent = t("unsaved_btn_discard_switch");
                this.unsavedModal.classList.remove('hidden');
                // Revert select display until decision
                this.activeSheetSelector.value = this.currentSheetName;
            } else {
                this.handleSwitchSheet(selectedSheet);
            }
        });

        // Feature 015: Catalog Header Source Change without Workspace Canvas Resets
        this.catalogSheetSelector.addEventListener('change', (e) => {
            this.catalogSheetName = e.target.value;
            this.filterAndRenderSidebar();
        });

        // Feature 015, 016 & 018: Unsaved Changes Modal Actions
        const closeUnsavedModal = () => {
            this.unsavedModal.classList.add('hidden');
            if (this.pendingAction && this.pendingAction.type === 'switch_sheet') {
                this.activeSheetSelector.value = this.currentSheetName;
            }
            this.pendingAction = null;
        };

        this.unsavedModalClose.addEventListener('click', closeUnsavedModal);
        this.btnUnsavedCancel.addEventListener('click', closeUnsavedModal);

        this.btnUnsavedDiscard.addEventListener('click', () => {
            const action = this.pendingAction;
            closeUnsavedModal();
            if (!action) return;

            this.isDirty = false;
            if (action.type === 'switch_sheet') {
                this.activeSheetSelector.value = action.targetSheet;
                this.handleSwitchSheet(action.targetSheet);
            } else if (action.type === 'import_file') {
                this.promptOpenAndImportFile();
            } else if (action.type === 'refresh_file') {
                this.performRefresh();
            }
        });

        this.btnUnsavedSave.addEventListener('click', async () => {
            const action = this.pendingAction;
            closeUnsavedModal();
            if (!action) return;

            const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
            if (this.currentTemplatePath) {
                // 1-Click Direct Sync to bound template
                try {
                    const res = await eel.save_template_sync(this.currentTemplatePath)();
                    if (res.success) {
                        this.isDirty = false;
                        this.updateTemplateBadge(res.template_path);
                        this.showToast(t('toast_template_updated', { template: res.template_path.split(/[/\\]/).pop() }), "success");
                        if (action.type === 'switch_sheet') {
                            this.activeSheetSelector.value = action.targetSheet;
                            this.handleSwitchSheet(action.targetSheet);
                        } else if (action.type === 'import_file') {
                            this.promptOpenAndImportFile();
                        } else if (action.type === 'refresh_file') {
                            this.performRefresh();
                        }
                    } else {
                        this.showToast(res.error || t("toast_template_failed"), "error");
                    }
                } catch (err) {
                    this.showToast("Error updating template: " + err, "error");
                }
            } else {
                // Initial save through dialog
                let defaultName = "Шаблон_reorganized_headers_export.xlsx";
                if (this.currentFileName) {
                    defaultName = `Шаблон_${this.currentFileName}`;
                }
                try {
                    const dialogRes = await eel.save_file_dialog(defaultName)();
                    if (dialogRes && dialogRes.success && !dialogRes.cancelled && dialogRes.file_path) {
                        const res = await eel.save_template_sync(dialogRes.file_path)();
                        if (res.success) {
                            this.isDirty = false;
                            this.updateTemplateBadge(res.template_path);
                            this.showToast(t('toast_template_saved', { template: res.template_path.split(/[/\\]/).pop() }), "success");
                            if (action.type === 'switch_sheet') {
                                this.activeSheetSelector.value = action.targetSheet;
                                this.handleSwitchSheet(action.targetSheet);
                            } else if (action.type === 'import_file') {
                                this.promptOpenAndImportFile();
                            } else if (action.type === 'refresh_file') {
                                this.performRefresh();
                            }
                        } else {
                            this.showToast(res.error || t("toast_template_failed"), "error");
                        }
                    } else {
                        this.showToast(t("toast_save_cancelled"), "info");
                    }
                } catch (err) {
                    this.showToast("Error saving before action: " + err, "error");
                }
            }
        });

        // Real-time Sidebar Search Input Event
        this.sidebarSearch.addEventListener('input', () => {
            this.filterAndRenderSidebar();
        });

        // Delegate click events on tree view (Feature 011 & 019: Chevron toggle, Add Child, Rename, Delete)
        this.treeViewEl.addEventListener('click', (e) => {
            const toggleBtn = e.target.closest('.node-toggle');
            if (toggleBtn) {
                const nodeId = toggleBtn.dataset.id;
                const treeNode = toggleBtn.closest('.tree-node');
                if (treeNode && nodeId) {
                    if (this.collapsedNodeIds.has(nodeId)) {
                        this.collapsedNodeIds.delete(nodeId);
                        treeNode.classList.remove('collapsed');
                        toggleBtn.title = "Collapse folder";
                    } else {
                        this.collapsedNodeIds.add(nodeId);
                        treeNode.classList.add('collapsed');
                        toggleBtn.title = "Expand folder";
                    }
                }
                return;
            }

            const renameBtn = e.target.closest('.action-btn.rename-node');
            if (renameBtn) {
                const nodeId = renameBtn.dataset.id;
                const nodeCard = renameBtn.closest('.tree-node');
                const titleEl = nodeCard ? nodeCard.querySelector('.node-title') : null;
                const currentName = titleEl ? titleEl.textContent.trim() : '';
                const currentType = nodeCard ? (nodeCard.dataset.dataType || 'Text') : 'Text';
                const isFolder = nodeCard ? (nodeCard.dataset.isFolder === 'true') : false;
                this.openEditModal(nodeId, currentName, currentType, isFolder);
                return;
            }

            const addRootCanvasBtn = e.target.closest('#btnAddRootCanvas, .btn-add-root-canvas');
            if (addRootCanvasBtn) {
                this.openAddModal(null, t("modal_create_title"));
                return;
            }

            const addBtn = e.target.closest('.action-btn.add-child');
            if (addBtn) {
                const parentId = addBtn.dataset.id;
                this.openAddModal(parentId, t("tooltip_add_child"));
                return;
            }

            const deleteBtn = e.target.closest('.action-btn.delete');
            if (deleteBtn) {
                const nodeId = deleteBtn.dataset.id;
                this.handleDeleteNode(nodeId);
                return;
            }
        });

        // Feature 019 & 020: Double-click on node label or badge to edit
        this.treeViewEl.addEventListener('dblclick', (e) => {
            const targetEl = e.target.closest('.node-title, .node-type-badge');
            if (targetEl) {
                const nodeCard = targetEl.closest('.tree-node');
                const nodeId = nodeCard ? nodeCard.dataset.id : null;
                const titleEl = nodeCard ? nodeCard.querySelector('.node-title') : null;
                const currentName = titleEl ? titleEl.textContent.trim() : '';
                const currentType = nodeCard ? (nodeCard.dataset.dataType || 'Text') : 'Text';
                const isFolder = nodeCard ? (nodeCard.dataset.isFolder === 'true') : false;
                if (nodeId) {
                    this.openEditModal(nodeId, currentName, currentType, isFolder);
                }
            }
        });


        // Modal event handlers
        document.getElementById('modalClose').addEventListener('click', () => this.closeModal());
        document.getElementById('btnModalCancel').addEventListener('click', () => this.closeModal());
        document.getElementById('btnModalSubmit').addEventListener('click', () => this.submitModal());
        this.inputNodeName.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') this.submitModal();
            if (e.key === 'Escape') this.closeModal();
        });
    },

    // Feature 013: Unified Tab Switching Controller
    bindTabs() {
        if (this.tabBtnCatalog && this.tabBtnPaths) {
            this.tabBtnCatalog.addEventListener('click', () => this.switchTab('catalog'));
            this.tabBtnPaths.addEventListener('click', () => this.switchTab('paths'));
        }
    },

    switchTab(tabName) {
        if (!this.tabBtnCatalog || !this.tabBtnPaths || !this.tabContentCatalog || !this.tabContentPaths) return;

        if (tabName === 'catalog') {
            this.tabBtnCatalog.classList.add('active');
            this.tabBtnPaths.classList.remove('active');
            this.tabContentCatalog.classList.remove('hidden');
            this.tabContentCatalog.classList.add('active');
            this.tabContentPaths.classList.add('hidden');
            this.tabContentPaths.classList.remove('active');
        } else {
            this.tabBtnPaths.classList.add('active');
            this.tabBtnCatalog.classList.remove('active');
            this.tabContentPaths.classList.remove('hidden');
            this.tabContentPaths.classList.add('active');
            this.tabContentCatalog.classList.add('hidden');
            this.tabContentCatalog.classList.remove('active');
        }
    },

    // Feature 013: Draggable Left-Edge Sidebar Resizing Controller
    bindResizer() {
        if (!this.sidebarResizer || !this.unifiedSidebar) return;

        // Restore persisted width from localStorage
        const savedWidth = localStorage.getItem('app_sidebar_width');
        if (savedWidth) {
            const parsed = parseInt(savedWidth, 10);
            if (!isNaN(parsed) && parsed >= 260) {
                this.setSidebarWidth(parsed);
            }
        }

        let isDragging = false;

        const onPointerMove = (e) => {
            if (!isDragging) return;
            e.preventDefault();
            const containerWidth = window.innerWidth;
            const newWidth = containerWidth - e.clientX;
            const minWidth = 260;
            const maxWidth = Math.max(minWidth, Math.min(containerWidth * 0.75, containerWidth - 320));
            const clampedWidth = Math.max(minWidth, Math.min(newWidth, maxWidth));
            this.setSidebarWidth(clampedWidth);
        };

        const onPointerUp = () => {
            if (!isDragging) return;
            isDragging = false;
            document.body.classList.remove('is-resizing');
            this.sidebarResizer.classList.remove('active');
            window.removeEventListener('pointermove', onPointerMove);
            window.removeEventListener('pointerup', onPointerUp);
            window.removeEventListener('pointercancel', onPointerUp);

            const currentWidth = this.unifiedSidebar.offsetWidth;
            if (currentWidth >= 260) {
                localStorage.setItem('app_sidebar_width', currentWidth.toString());
            }
        };

        this.sidebarResizer.addEventListener('pointerdown', (e) => {
            if (e.button !== 0) return;
            isDragging = true;
            document.body.classList.add('is-resizing');
            this.sidebarResizer.classList.add('active');

            window.addEventListener('pointermove', onPointerMove);
            window.addEventListener('pointerup', onPointerUp);
            window.addEventListener('pointercancel', onPointerUp);
        });

        this.sidebarResizer.addEventListener('dblclick', () => {
            const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
            this.setSidebarWidth(340);
            localStorage.setItem('app_sidebar_width', '340');
            this.showToast(t("sidebar_width_reset_toast"), "success");
        });
    },

    setSidebarWidth(width) {
        if (this.unifiedSidebar) {
            this.unifiedSidebar.style.setProperty('--sidebar-width', `${width}px`);
            this.unifiedSidebar.style.width = `${width}px`;
        }
    },

    updateSheetSelectorsLabels() {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        if (this.catalogSheetSelector) {
            const allOpt = this.catalogSheetSelector.querySelector('option[value="__ALL__"]');
            if (allOpt) allOpt.textContent = t('catalog_all_sheets');
            const emptyOpt = this.catalogSheetSelector.querySelector('option[value=""]');
            if (emptyOpt) emptyOpt.textContent = t('catalog_no_file');
        }
        if (this.activeSheetSelector) {
            const emptyOpt = this.activeSheetSelector.querySelector('option[value=""]');
            if (emptyOpt) emptyOpt.textContent = t('workspace_no_sheet');
        }
    },

    async refreshWorkspace() {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        if (!this.currentFileName) {
            this.showToast(t("toast_refresh_no_session"), "warning");
            return;
        }

        if (this.isDirty) {
            this.pendingAction = { type: 'refresh_file' };
            if (this.currentTemplatePath) {
                const base = this.currentTemplatePath.split(/[/\\]/).pop();
                this.unsavedModalMessage.innerHTML = t('unsaved_msg_refresh_update', { template: this.escapeHtml(base), file: this.escapeHtml(this.currentFileName) });
                this.btnUnsavedSave.textContent = t("unsaved_btn_update_refresh");
            } else {
                this.unsavedModalMessage.innerHTML = t('unsaved_msg_refresh_save', { file: this.escapeHtml(this.currentFileName) });
                this.btnUnsavedSave.textContent = t("unsaved_btn_save_refresh");
            }
            this.btnUnsavedDiscard.textContent = t("unsaved_btn_discard_refresh");
            this.unsavedModal.classList.remove('hidden');
        } else {
            await this.performRefresh();
        }
    },

    async performRefresh() {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        if (typeof eel === 'undefined' || !eel.refresh_excel_session) {
            console.warn("Eel backend not connected.");
            return;
        }

        try {
            const res = await eel.refresh_excel_session()();
            if (res && res.success) {
                this.isDirty = false;
                this.cachedAllHeaders = res.all_headers || {};
                this.cachedAllHeadersMeta = res.all_headers_meta || {};

                // Update Active Sheet Selector
                this.activeSheetSelector.innerHTML = '';
                res.sheets.forEach(sheetName => {
                    const option = document.createElement('option');
                    option.value = sheetName;
                    option.textContent = sheetName;
                    if (sheetName === res.active_sheet) option.selected = true;
                    this.activeSheetSelector.appendChild(option);
                });

                // Update Catalog Header Source Selector
                this.catalogSheetSelector.innerHTML = '';
                const allOpt = document.createElement('option');
                allOpt.value = '__ALL__';
                allOpt.textContent = t('catalog_all_sheets');
                this.catalogSheetSelector.appendChild(allOpt);

                res.sheets.forEach(sheetName => {
                    const option = document.createElement('option');
                    option.value = sheetName;
                    option.textContent = sheetName;
                    if (sheetName === res.active_sheet) option.selected = true;
                    this.catalogSheetSelector.appendChild(option);
                });

                this.currentFileName = res.file_path.split(/[/\\]/).pop();
                this.currentSheetName = res.active_sheet;
                this.catalogSheetName = res.active_sheet;
                this.currentRawHeaders = res.headers || [];
                this.currentRawHeadersMeta = res.headers_meta || [];

                this.updateTemplateBadge(res.template_path);
                this.catalogSheetSelector.disabled = false;
                this.sidebarSearch.disabled = false;
                this.sidebarSearch.value = '';
                this.collapsedNodeIds.clear();
                this.filterAndRenderSidebar();
                if (res.roots) {
                    this.updateUI(res.roots);
                }
                this.showToast(t('toast_refreshed_session', { file: this.currentFileName }), "success");
            } else {
                this.showToast(res.error || t("toast_refresh_failed"), "error");
            }
        } catch (err) {
            this.showToast("RPC Error refreshing session: " + err, "error");
        }
    },

    updateUI(roots) {
        this.currentRoots = roots || [];
        TreeRenderer.renderTree(roots, this.treeViewEl, this.collapsedNodeIds);
        TreeRenderer.renderPaths(roots, this.pathListEl);

        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        let totalNodes = 0;
        function countNodes(node) {
            totalNodes++;
            if (node.children) node.children.forEach(countNodes);
        }
        if (roots) roots.forEach(countNodes);

        this.nodeCountBadge.textContent = t('node_count', { count: totalNodes });
    },

    // Feature 011: Expand All and Collapse All Global Controls
    expandAll() {
        this.collapsedNodeIds.clear();
        this.updateUI(this.currentRoots);
    },

    collapseAll() {
        this.collapsedNodeIds.clear();
        const collectFolders = (node) => {
            if (node.children && node.children.length > 0) {
                this.collapsedNodeIds.add(node.id);
                node.children.forEach(collectFolders);
            }
        };
        if (this.currentRoots) {
            this.currentRoots.forEach(collectFolders);
        }
        this.updateUI(this.currentRoots);
    },

    // Feature 002, 006 & 015: Excel File Import & Dual-Selector Sheet Management
    async handleImportExcelFile(filePath) {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        try {
            const res = await eel.import_excel_file(filePath)();
            if (res.success) {
                this.isDirty = false;
                this.cachedAllHeaders = res.all_headers || {};
                this.cachedAllHeadersMeta = res.all_headers_meta || {};

                // Populate Active Workspace Sheet Selector
                this.activeSheetSelector.innerHTML = '';
                res.sheets.forEach(sheetName => {
                    const option = document.createElement('option');
                    option.value = sheetName;
                    option.textContent = sheetName;
                    if (sheetName === res.active_sheet) option.selected = true;
                    this.activeSheetSelector.appendChild(option);
                });

                // Populate Catalog Header Source Selector with All Sheets + individual sheets
                this.catalogSheetSelector.innerHTML = '';
                const allOpt = document.createElement('option');
                allOpt.value = '__ALL__';
                allOpt.textContent = t('catalog_all_sheets');
                this.catalogSheetSelector.appendChild(allOpt);

                res.sheets.forEach(sheetName => {
                    const option = document.createElement('option');
                    option.value = sheetName;
                    option.textContent = sheetName;
                    if (sheetName === res.active_sheet) option.selected = true;
                    this.catalogSheetSelector.appendChild(option);
                });

                this.currentFileName = filePath.split(/[/\\]/).pop();
                this.currentSheetName = res.active_sheet;
                this.catalogSheetName = res.active_sheet;
                this.currentRawHeaders = res.headers || [];
                this.currentRawHeadersMeta = res.headers_meta || [];

                this.updateTemplateBadge(res.template_path);
                this.catalogSheetSelector.disabled = false;
                this.sidebarSearch.disabled = false;
                this.sidebarSearch.value = '';
                this.collapsedNodeIds.clear(); // Reset collapse state on new file import
                this.filterAndRenderSidebar();
                if (res.roots) {
                    this.updateUI(res.roots);
                }
                this.showToast(t('toast_imported_session', { count: res.sheets.length }), "success");
            } else {
                this.showToast(res.error || t("toast_import_failed"), "error");
            }
        } catch (err) {
            this.showToast("RPC Error importing file: " + err, "error");
        }
    },

    async handleSwitchSheet(sheetName) {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        try {
            const res = await eel.switch_active_sheet(sheetName)();
            if (res.success) {
                this.isDirty = false;
                this.currentSheetName = res.sheet_name;
                this.activeSheetSelector.value = res.sheet_name;
                this.updateTemplateBadge(res.template_path);
                this.currentRawHeaders = res.headers || [];
                this.sidebarSearch.value = '';
                this.collapsedNodeIds.clear(); // Reset collapse state on sheet switch
                this.filterAndRenderSidebar();
                if (res.roots) {
                    this.updateUI(res.roots);
                }
                this.showToast(t('toast_switched_sheet', { sheet: sheetName }), "success");
            } else {
                this.showToast(res.error || t("toast_switch_failed"), "error");
            }
        } catch (err) {
            this.showToast("RPC Error switching sheet: " + err, "error");
        }
    },

    filterAndRenderSidebar() {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        let headerItems = [];
        const sourceSheet = this.catalogSheetName || this.currentSheetName;

        if (sourceSheet === '__ALL__') {
            // Aggregate headers from all cached sheets with sheet tags and data types
            if (this.cachedAllHeadersMeta && Object.keys(this.cachedAllHeadersMeta).length > 0) {
                Object.entries(this.cachedAllHeadersMeta).forEach(([sName, items]) => {
                    items.forEach(it => {
                        headerItems.push({ label: it.name, type: it.type || 'Text', sheet: sName });
                    });
                });
            } else {
                Object.entries(this.cachedAllHeaders).forEach(([sName, headers]) => {
                    headers.forEach(h => {
                        headerItems.push({ label: h, type: 'Text', sheet: sName });
                    });
                });
            }
        } else if (this.cachedAllHeadersMeta && this.cachedAllHeadersMeta[sourceSheet]) {
            headerItems = this.cachedAllHeadersMeta[sourceSheet].map(it => ({ label: it.name, type: it.type || 'Text', sheet: null }));
        } else if (this.cachedAllHeaders && this.cachedAllHeaders[sourceSheet]) {
            headerItems = this.cachedAllHeaders[sourceSheet].map(h => ({ label: h, type: 'Text', sheet: null }));
        } else {
            headerItems = this.currentRawHeaders.map(h => ({ label: h, type: 'Text', sheet: null }));
        }

        const query = this.sidebarSearch.value.trim().toLowerCase();
        const filtered = query
            ? headerItems.filter(item => item.label.toLowerCase().includes(query) || (item.sheet && item.sheet.toLowerCase().includes(query)) || (item.type && item.type.toLowerCase().includes(query)))
            : headerItems;

        this.sidebarHeaderList.innerHTML = '';

        if (!filtered || filtered.length === 0) {
            this.sidebarEmptyState.classList.remove('hidden');
            this.sidebarEmptyState.style.display = '';
            this.sidebarHeaderList.classList.add('hidden');
            this.headerCountBadge.textContent = t('header_count', { count: 0 });
            return;
        }

        this.sidebarEmptyState.classList.add('hidden');
        this.sidebarEmptyState.style.display = 'none';
        this.sidebarHeaderList.classList.remove('hidden');

        filtered.forEach(item => {
            const itemEl = document.createElement('div');
            itemEl.className = 'sidebar-header-item';
            itemEl.dataset.headerLabel = item.label;
            itemEl.dataset.dataType = item.type || 'Text';
            const itemTypeLabel = window.I18n ? I18n.getTypeLabel(item.type) : (item.type || 'Text');
            const sheetTagHtml = item.sheet ? `<span class="header-sheet-tag">${this.escapeHtml(item.sheet)}</span>` : '';
            const typeTagHtml = `<span class="header-type-tag" title="${t('tooltip_data_type_badge')}">${this.escapeHtml(itemTypeLabel)}</span>`;

            itemEl.innerHTML = `
                <div style="display: flex; align-items: center; gap: 4px; overflow: hidden; flex: 1;">
                    <span class="header-title">${this.escapeHtml(item.label)}</span>
                    ${typeTagHtml}
                    ${sheetTagHtml}
                </div>
                <span class="drag-badge" title="${t('tooltip_drag_handle')}">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="9" cy="5" r="1"/><circle cx="9" cy="12" r="1"/><circle cx="9" cy="19" r="1"/>
                        <circle cx="15" cy="5" r="1"/><circle cx="15" cy="12" r="1"/><circle cx="15" cy="19" r="1"/>
                    </svg>
                </span>
            `;

            DragDropHandler.bindSidebarItem(itemEl);
            this.sidebarHeaderList.appendChild(itemEl);
        });

        this.headerCountBadge.textContent = t('header_count', { count: filtered.length });
    },

    async handleDropPayload(payload, targetId, zone) {
        if (!payload) return;

        // Feature 011: Auto-expand folder when dropping a child inside it
        if (zone === 'NEST_CHILD' && targetId) {
            this.collapsedNodeIds.delete(targetId);
        }

        if (payload.isNew) {
            await this.handleAddHeaderNode(payload.label, targetId, zone, payload.dataType || 'Text');
        } else if (payload.id) {
            if (!targetId || !zone) return;
            await this.handleMoveNode(payload.id, targetId, zone);
        }
    },

    // Feature 002 & 020: Add Header from Non-Destructive Drag and Drop with zone positioning and data type inheritance
    async handleAddHeaderNode(headerLabel, targetId, zone, dataType = "Text") {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        try {
            const res = await eel.add_node(null, headerLabel, false, targetId, zone, dataType)();
            if (res.success) {
                this.isDirty = true;
                this.updateUI(res.roots);
                this.showToast(t('toast_header_added', { name: headerLabel, type: dataType }), "success");
            } else {
                this.showToast(res.error || "Failed to add header node.", "error");
            }
        } catch (err) {
            this.showToast("RPC Error adding header node: " + err, "error");
        }
    },

    // Feature 002 & 014: Reconstructed Tree Row 1 Horizontal Clean Template Export
    async handleExportReorganizedRow1(outputPath) {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        if (!this.currentSheetName) {
            this.showToast(t("toast_refresh_no_session"), "warning");
            return false;
        }

        // Collect leaf path strings from rendered path cards
        const pathElements = this.pathListEl.querySelectorAll('.path-card');
        const leafPaths = Array.from(pathElements).map(el => el.textContent.trim()).filter(Boolean);

        if (leafPaths.length === 0) {
            this.showToast(t("toast_tree_empty_export"), "warning");
            return false;
        }

        try {
            const res = await eel.export_reorganized_row1(this.currentSheetName, leafPaths, outputPath)();
            if (res.success) {
                this.isDirty = false;
                this.showToast(t('toast_template_exported', { template: outputPath }), "success");
                return true;
            } else {
                this.showToast(res.error || t("toast_template_failed"), "error");
                return false;
            }
        } catch (err) {
            this.showToast("RPC Error exporting Row 1: " + err, "error");
            return false;
        }
    },

    openAddModal(parentId, title) {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        this.modalMode = 'create';
        this.activeParentIdForModal = parentId;
        this.activeNodeIdForEdit = null;
        this.modalTitle.textContent = title || t("modal_create_title");
        if (this.btnModalSubmit) this.btnModalSubmit.textContent = t("modal_btn_create");
        this.inputNodeName.value = '';
        if (this.selectNodeType) {
            this.selectNodeType.value = 'Text';
            this.selectNodeType.disabled = false;
            this.selectNodeType.classList.remove('hidden');
        }
        if (this.folderTypeHint) this.folderTypeHint.classList.add('hidden');
        this.nodeModal.classList.remove('hidden');
        this.inputNodeName.focus();
    },

    openEditModal(nodeId, currentName, currentType = 'Text', isFolder = false) {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        this.modalMode = 'edit';
        this.activeNodeIdForEdit = nodeId;
        this.activeParentIdForModal = null;
        this.modalTitle.textContent = isFolder ? t("modal_edit_folder_title") : t("modal_edit_element_title");
        if (this.btnModalSubmit) this.btnModalSubmit.textContent = t("modal_btn_save");
        this.inputNodeName.value = currentName || '';

        if (this.selectNodeType) {
            this.selectNodeType.value = currentType || 'Text';
            if (isFolder) {
                this.selectNodeType.disabled = true;
                this.selectNodeType.classList.add('hidden');
                if (this.folderTypeHint) this.folderTypeHint.classList.remove('hidden');
            } else {
                this.selectNodeType.disabled = false;
                this.selectNodeType.classList.remove('hidden');
                if (this.folderTypeHint) this.folderTypeHint.classList.add('hidden');
            }
        }

        this.nodeModal.classList.remove('hidden');
        this.inputNodeName.focus();
        this.inputNodeName.select();
    },

    closeModal() {
        this.nodeModal.classList.add('hidden');
        this.activeParentIdForModal = null;
        this.activeNodeIdForEdit = null;
        this.modalMode = 'create';
    },

    async submitModal() {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        const name = this.inputNodeName.value.trim();
        if (!name) {
            this.showToast(t("toast_name_empty"), "warning");
            return;
        }

        const selectedType = (this.selectNodeType && !this.selectNodeType.disabled) ? this.selectNodeType.value : 'Text';

        if (this.modalMode === 'edit') {
            try {
                const res = await eel.update_node(this.activeNodeIdForEdit, name, selectedType)();
                if (res.success) {
                    this.isDirty = true;
                    this.updateUI(res.roots);
                    this.closeModal();
                    this.showToast(t('toast_node_updated', { name: name }), "success");
                } else {
                    this.showToast(res.error || "Failed to update node.", "error");
                }
            } catch (err) {
                this.showToast("RPC Error updating node: " + err, "error");
            }
        } else {
            try {
                const res = await eel.add_node(this.activeParentIdForModal, name, true, null, null, selectedType)();
                if (res.success) {
                    this.isDirty = true;
                    this.updateUI(res.roots);
                    this.closeModal();
                    this.showToast(t('toast_node_created', { name: name }), "success");
                } else {
                    this.showToast(res.error || "Failed to add node.", "error");
                }
            } catch (err) {
                this.showToast("RPC Error adding node: " + err, "error");
            }
        }
    },

    async handleMoveNode(nodeId, targetId, zone) {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        try {
            const res = await eel.move_node(nodeId, targetId, zone)();
            if (res.success) {
                this.isDirty = true;
                this.updateUI(res.roots);
            } else {
                this.showToast(res.rejection_reason || t("toast_move_rejected"), "warning");
            }
        } catch (err) {
            this.showToast("RPC Error moving node: " + err, "error");
        }
    },

    async handleDeleteNode(nodeId) {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        if (!confirm(t("confirm_delete"))) return;

        try {
            const res = await eel.delete_node(nodeId)();
            if (res.success) {
                this.isDirty = true;
                this.updateUI(res.roots);
                this.showToast(t("toast_node_deleted"), "success");
            } else {
                this.showToast(res.error || "Failed to delete node.", "error");
            }
        } catch (err) {
            this.showToast("RPC Error deleting node: " + err, "error");
        }
    },

    escapeHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    },

    showToast(message, type = 'warning') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        this.toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3500);
    }
};
