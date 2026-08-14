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
    pendingAction: null,
    isDirty: false,
    currentTemplatePath: null,
    currentRawHeaders: [],
    collapsedNodeIds: new Set(),
    currentRoots: [],

    async init() {
        this.collapsedNodeIds = new Set();
        this.currentRoots = [];
        this.cachedAllHeaders = {};
        this.isDirty = false;
        this.currentTemplatePath = null;
        this.pendingAction = null;
        this.modalMode = 'create';
        this.activeNodeIdForEdit = null;
        this.bindDOM();
        this.bindEvents();
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
        this.btnModalSubmit = document.getElementById('btnModalSubmit');

        // Toolbar Collapse / Expand buttons (Feature 011)
        this.btnExpandAll = document.getElementById('btnExpandAll');
        this.btnCollapseAll = document.getElementById('btnCollapseAll');

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
        if (this.templateStatusBadge) {
            if (this.currentTemplatePath) {
                const base = this.currentTemplatePath.split(/[/\\]/).pop();
                this.templateStatusBadge.textContent = `Template: ${base} (Synced)`;
                this.templateStatusBadge.title = `Bound Template File: ${this.currentTemplatePath}`;
            } else {
                this.templateStatusBadge.textContent = `Template: (None)`;
                this.templateStatusBadge.title = `No template file bound yet. Export or Save to bind.`;
            }
        }
    },

    bindEvents() {
        this.bindTabs();
        this.bindResizer();

        const btnCreateRootEmpty = document.getElementById('btnCreateRootEmpty');
        if (btnCreateRootEmpty) {
            btnCreateRootEmpty.addEventListener('click', () => this.openAddModal(null, "Create Root Node"));
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
                    this.unsavedModalMessage.innerHTML = `You have unsaved changes in your current session. Update template "<strong>${this.escapeHtml(base)}</strong>" before importing a new file?`;
                    this.btnUnsavedSave.textContent = "Update Template & Import";
                } else {
                    this.unsavedModalMessage.innerHTML = `You have unsaved changes in your current session. Save your changes to a template file before importing a new file?`;
                    this.btnUnsavedSave.textContent = "Save Template & Import";
                }
                this.btnUnsavedDiscard.textContent = "Discard & Import";
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
                        this.showToast(`Exported clean template to '${res.template_path.split(/[/\\]/).pop()}'.`, "success");
                    } else {
                        this.showToast(res.error || "Failed to export template.", "error");
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
                    this.unsavedModalMessage.innerHTML = `You have unsaved changes on sheet "<strong>${this.escapeHtml(this.currentSheetName || 'Active Sheet')}</strong>". Update template "<strong>${this.escapeHtml(base)}</strong>" before switching to "<strong>${this.escapeHtml(selectedSheet)}</strong>"?`;
                    this.btnUnsavedSave.textContent = "Update Template & Switch";
                } else {
                    this.unsavedModalMessage.innerHTML = `You have unsaved changes on sheet "<strong>${this.escapeHtml(this.currentSheetName || 'Active Sheet')}</strong>". Save your changes to a template file before switching to "<strong>${this.escapeHtml(selectedSheet)}</strong>"?`;
                    this.btnUnsavedSave.textContent = "Save Template & Switch";
                }
                this.btnUnsavedDiscard.textContent = "Discard & Switch";
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
            }
        });

        this.btnUnsavedSave.addEventListener('click', async () => {
            const action = this.pendingAction;
            closeUnsavedModal();
            if (!action) return;

            if (this.currentTemplatePath) {
                // 1-Click Direct Sync to bound template
                try {
                    const res = await eel.save_template_sync(this.currentTemplatePath)();
                    if (res.success) {
                        this.isDirty = false;
                        this.updateTemplateBadge(res.template_path);
                        this.showToast(`Updated template '${res.template_path.split(/[/\\]/).pop()}'.`, "success");
                        if (action.type === 'switch_sheet') {
                            this.activeSheetSelector.value = action.targetSheet;
                            this.handleSwitchSheet(action.targetSheet);
                        } else if (action.type === 'import_file') {
                            this.promptOpenAndImportFile();
                        }
                    } else {
                        this.showToast(res.error || "Failed to update template.", "error");
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
                            this.showToast(`Saved template '${res.template_path.split(/[/\\]/).pop()}'.`, "success");
                            if (action.type === 'switch_sheet') {
                                this.activeSheetSelector.value = action.targetSheet;
                                this.handleSwitchSheet(action.targetSheet);
                            } else if (action.type === 'import_file') {
                                this.promptOpenAndImportFile();
                            }
                        } else {
                            this.showToast(res.error || "Failed to save template.", "error");
                        }
                    } else {
                        this.showToast("Save cancelled. Remained on active workspace.", "info");
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
                this.openEditModal(nodeId, currentName);
                return;
            }

            const addBtn = e.target.closest('.action-btn.add-child');
            if (addBtn) {
                const parentId = addBtn.dataset.id;
                this.openAddModal(parentId, "Add Child Node");
                return;
            }

            const deleteBtn = e.target.closest('.action-btn.delete');
            if (deleteBtn) {
                const nodeId = deleteBtn.dataset.id;
                this.handleDeleteNode(nodeId);
                return;
            }
        });

        // Feature 019: Double-click on node label to rename
        this.treeViewEl.addEventListener('dblclick', (e) => {
            const titleEl = e.target.closest('.node-title');
            if (titleEl) {
                const nodeId = titleEl.dataset.id;
                const currentName = titleEl.textContent.trim();
                if (nodeId) {
                    this.openEditModal(nodeId, currentName);
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
            this.setSidebarWidth(340);
            localStorage.setItem('app_sidebar_width', '340');
            this.showToast("Sidebar width reset to default (340px).", "success");
        });
    },

    setSidebarWidth(width) {
        if (this.unifiedSidebar) {
            this.unifiedSidebar.style.setProperty('--sidebar-width', `${width}px`);
            this.unifiedSidebar.style.width = `${width}px`;
        }
    },

    async refreshWorkspace() {
        if (typeof eel === 'undefined' || !eel.get_workspace_tree) {
            console.warn("Eel backend not connected.");
            return;
        }

        try {
            const res = await eel.get_workspace_tree()();
            if (res && res.success) {
                this.updateUI(res.roots);
            }
        } catch (err) {
            console.error("Error fetching workspace tree:", err);
        }
    },

    updateUI(roots) {
        this.currentRoots = roots || [];
        TreeRenderer.renderTree(roots, this.treeViewEl, this.collapsedNodeIds);
        TreeRenderer.renderPaths(roots, this.pathListEl);

        let totalNodes = 0;
        function countNodes(node) {
            totalNodes++;
            if (node.children) node.children.forEach(countNodes);
        }
        if (roots) roots.forEach(countNodes);

        this.nodeCountBadge.textContent = `${totalNodes} Nodes`;
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
        try {
            const res = await eel.import_excel_file(filePath)();
            if (res.success) {
                this.isDirty = false;
                this.cachedAllHeaders = res.all_headers || {};

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
                allOpt.textContent = 'All Sheets (Combined)';
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

                this.updateTemplateBadge(res.template_path);
                this.catalogSheetSelector.disabled = false;
                this.sidebarSearch.disabled = false;
                this.sidebarSearch.value = '';
                this.collapsedNodeIds.clear(); // Reset collapse state on new file import
                this.filterAndRenderSidebar();
                if (res.roots) {
                    this.updateUI(res.roots);
                }
                this.showToast(`Imported Excel session: ${res.sheets.length} sheets found.`, "success");
            } else {
                this.showToast(res.error || "Failed to import Excel session.", "error");
            }
        } catch (err) {
            this.showToast("RPC Error importing file: " + err, "error");
        }
    },

    async handleSwitchSheet(sheetName) {
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
                this.showToast(`Switched active workspace sheet to '${sheetName}'.`, "success");
            } else {
                this.showToast(res.error || "Failed to switch sheet.", "error");
            }
        } catch (err) {
            this.showToast("RPC Error switching sheet: " + err, "error");
        }
    },

    filterAndRenderSidebar() {
        let headerItems = [];
        const sourceSheet = this.catalogSheetName || this.currentSheetName;

        if (sourceSheet === '__ALL__') {
            // Aggregate headers from all cached sheets with sheet tags
            Object.entries(this.cachedAllHeaders).forEach(([sName, headers]) => {
                headers.forEach(h => {
                    headerItems.push({ label: h, sheet: sName });
                });
            });
        } else if (this.cachedAllHeaders && this.cachedAllHeaders[sourceSheet]) {
            headerItems = this.cachedAllHeaders[sourceSheet].map(h => ({ label: h, sheet: null }));
        } else {
            headerItems = this.currentRawHeaders.map(h => ({ label: h, sheet: null }));
        }

        const query = this.sidebarSearch.value.trim().toLowerCase();
        const filtered = query
            ? headerItems.filter(item => item.label.toLowerCase().includes(query) || (item.sheet && item.sheet.toLowerCase().includes(query)))
            : headerItems;

        this.sidebarHeaderList.innerHTML = '';

        if (!filtered || filtered.length === 0) {
            this.sidebarEmptyState.classList.remove('hidden');
            this.sidebarEmptyState.style.display = '';
            this.sidebarHeaderList.classList.add('hidden');
            this.headerCountBadge.textContent = "0 Headers";
            return;
        }

        this.sidebarEmptyState.classList.add('hidden');
        this.sidebarEmptyState.style.display = 'none';
        this.sidebarHeaderList.classList.remove('hidden');

        filtered.forEach(item => {
            const itemEl = document.createElement('div');
            itemEl.className = 'sidebar-header-item';
            itemEl.dataset.headerLabel = item.label;

            const sheetTagHtml = item.sheet ? `<span class="header-sheet-tag">${this.escapeHtml(item.sheet)}</span>` : '';

            itemEl.innerHTML = `
                <span class="header-title">${this.escapeHtml(item.label)}</span>
                ${sheetTagHtml}
                <span class="drag-badge" title="Drag to tree constructor">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="9" cy="5" r="1"/><circle cx="9" cy="12" r="1"/><circle cx="9" cy="19" r="1"/>
                        <circle cx="15" cy="5" r="1"/><circle cx="15" cy="12" r="1"/><circle cx="15" cy="19" r="1"/>
                    </svg>
                </span>
            `;

            DragDropHandler.bindSidebarItem(itemEl);
            this.sidebarHeaderList.appendChild(itemEl);
        });

        this.headerCountBadge.textContent = `${filtered.length} Headers`;
    },

    async handleDropPayload(payload, targetId, zone) {
        if (!payload) return;

        // Feature 011: Auto-expand folder when dropping a child inside it
        if (zone === 'NEST_CHILD' && targetId) {
            this.collapsedNodeIds.delete(targetId);
        }

        if (payload.isNew) {
            await this.handleAddHeaderNode(payload.label, targetId, zone);
        } else if (payload.id) {
            if (!targetId || !zone) return;
            await this.handleMoveNode(payload.id, targetId, zone);
        }
    },

    // Feature 002: Add Header from Non-Destructive Drag and Drop with zone positioning
    async handleAddHeaderNode(headerLabel, targetId, zone) {
        try {
            const res = await eel.add_node(null, headerLabel, false, targetId, zone)();
            if (res.success) {
                this.isDirty = true;
                this.updateUI(res.roots);
                this.showToast(`Added header node '${headerLabel}' into tree structure.`, "success");
            } else {
                this.showToast(res.error || "Failed to add header node.", "error");
            }
        } catch (err) {
            this.showToast("RPC Error adding header node: " + err, "error");
        }
    },

    // Feature 002 & 014: Reconstructed Tree Row 1 Horizontal Clean Template Export
    async handleExportReorganizedRow1(outputPath) {
        if (!this.currentSheetName) {
            this.showToast("Please import an Excel file session first.", "warning");
            return false;
        }

        // Collect leaf path strings from rendered path cards
        const pathElements = this.pathListEl.querySelectorAll('.path-card');
        const leafPaths = Array.from(pathElements).map(el => el.textContent.trim()).filter(Boolean);

        if (leafPaths.length === 0) {
            this.showToast("Tree is empty. Add nodes before exporting.", "warning");
            return false;
        }

        try {
            const res = await eel.export_reorganized_row1(this.currentSheetName, leafPaths, outputPath)();
            if (res.success) {
                this.isDirty = false;
                this.showToast(`Exported ${res.column_count} leaf path columns to '${this.currentSheetName}' in Row 1.`, "success");
                return true;
            } else {
                this.showToast(res.error || "Failed to export Row 1 paths.", "error");
                return false;
            }
        } catch (err) {
            this.showToast("RPC Error exporting Row 1: " + err, "error");
            return false;
        }
    },

    openAddModal(parentId, title) {
        this.modalMode = 'create';
        this.activeParentIdForModal = parentId;
        this.activeNodeIdForEdit = null;
        this.modalTitle.textContent = title || "Create Node";
        if (this.btnModalSubmit) this.btnModalSubmit.textContent = "Create Node";
        this.inputNodeName.value = '';
        this.nodeModal.classList.remove('hidden');
        this.inputNodeName.focus();
    },

    openEditModal(nodeId, currentName) {
        this.modalMode = 'edit';
        this.activeNodeIdForEdit = nodeId;
        this.activeParentIdForModal = null;
        this.modalTitle.textContent = "Edit Node Name";
        if (this.btnModalSubmit) this.btnModalSubmit.textContent = "Save Changes";
        this.inputNodeName.value = currentName || '';
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
        const name = this.inputNodeName.value.trim();
        if (!name) {
            this.showToast("Node name cannot be empty.", "warning");
            return;
        }

        if (this.modalMode === 'edit') {
            try {
                const res = await eel.rename_node(this.activeNodeIdForEdit, name)();
                if (res.success) {
                    this.isDirty = true;
                    this.updateUI(res.roots);
                    this.closeModal();
                    this.showToast(`Node renamed to '${name}'.`, "success");
                } else {
                    this.showToast(res.error || "Failed to rename node.", "error");
                }
            } catch (err) {
                this.showToast("RPC Error renaming node: " + err, "error");
            }
        } else {
            try {
                const res = await eel.add_node(this.activeParentIdForModal, name)();
                if (res.success) {
                    this.isDirty = true;
                    this.updateUI(res.roots);
                    this.closeModal();
                    this.showToast(`Node '${name}' created successfully.`, "success");
                } else {
                    this.showToast(res.error || "Failed to add node.", "error");
                }
            } catch (err) {
                this.showToast("RPC Error adding node: " + err, "error");
            }
        }
    },

    async handleMoveNode(nodeId, targetId, zone) {
        try {
            const res = await eel.move_node(nodeId, targetId, zone)();
            if (res.success) {
                this.isDirty = true;
                this.updateUI(res.roots);
            } else {
                this.showToast(res.rejection_reason || "Move rejected by backend.", "warning");
            }
        } catch (err) {
            this.showToast("RPC Error moving node: " + err, "error");
        }
    },

    async handleDeleteNode(nodeId) {
        if (!confirm("Are you sure you want to delete this node and all its contents?")) return;

        try {
            const res = await eel.delete_node(nodeId)();
            if (res.success) {
                this.isDirty = true;
                this.updateUI(res.roots);
                this.showToast("Node deleted.", "success");
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
