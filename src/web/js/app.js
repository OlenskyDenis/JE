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
    currentSheetName: null,
    currentRawHeaders: [],
    collapsedNodeIds: new Set(),
    currentRoots: [],

    async init() {
        this.collapsedNodeIds = new Set();
        this.currentRoots = [];
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
        this.toastContainer = document.getElementById('toastContainer');
        this.nodeModal = document.getElementById('nodeModal');
        this.modalTitle = document.getElementById('modalTitle');
        this.inputNodeName = document.getElementById('inputNodeName');

        // Toolbar Collapse / Expand buttons (Feature 011)
        this.btnExpandAll = document.getElementById('btnExpandAll');
        this.btnCollapseAll = document.getElementById('btnCollapseAll');

        // Sidebar DOM elements (Feature 002)
        this.sheetSelector = document.getElementById('sheetSelector');
        this.sidebarSearch = document.getElementById('sidebarSearch');
        this.sidebarHeaderList = document.getElementById('sidebarHeaderList');
        this.sidebarEmptyState = document.getElementById('sidebarEmptyState');
        this.headerCountBadge = document.getElementById('headerCountBadge');
    },

    bindEvents() {
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

        // Feature 003: Native OS Open File Dialog for Excel Import
        document.getElementById('btnImportExcel').addEventListener('click', async () => {
            try {
                const dialogRes = await eel.open_file_dialog()();
                if (dialogRes && dialogRes.success && !dialogRes.cancelled && dialogRes.file_path) {
                    this.handleImportExcelFile(dialogRes.file_path);
                }
            } catch (err) {
                this.showToast("RPC Error opening file dialog: " + err, "error");
            }
        });

        // Feature 003: Native OS Save File Dialog for Excel Export
        document.getElementById('btnExportExcel').addEventListener('click', async () => {
            try {
                const dialogRes = await eel.save_file_dialog("reorganized_headers_export.xlsx")();
                if (dialogRes && dialogRes.success && !dialogRes.cancelled && dialogRes.file_path) {
                    this.handleExportReorganizedRow1(dialogRes.file_path);
                }
            } catch (err) {
                this.showToast("RPC Error opening save dialog: " + err, "error");
            }
        });

        // Sheet Selector Change Event
        this.sheetSelector.addEventListener('change', (e) => {
            const selectedSheet = e.target.value;
            if (selectedSheet) {
                this.handleSwitchSheet(selectedSheet);
            }
        });

        // Real-time Sidebar Search Input Event
        this.sidebarSearch.addEventListener('input', () => {
            this.filterAndRenderSidebar();
        });

        // Delegate click events on tree view (Feature 011: Chevron toggle, Add Child, Delete)
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

        // Modal event handlers
        document.getElementById('modalClose').addEventListener('click', () => this.closeModal());
        document.getElementById('btnModalCancel').addEventListener('click', () => this.closeModal());
        document.getElementById('btnModalSubmit').addEventListener('click', () => this.submitAddModal());
        this.inputNodeName.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') this.submitAddModal();
        });
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

    // Feature 002 & 006: Excel File Import & Sheet Management with Automatic Tree Generation
    async handleImportExcelFile(filePath) {
        try {
            const res = await eel.import_excel_file(filePath)();
            if (res.success) {
                this.sheetSelector.innerHTML = '';
                res.sheets.forEach(sheetName => {
                    const option = document.createElement('option');
                    option.value = sheetName;
                    option.textContent = sheetName;
                    if (sheetName === res.active_sheet) option.selected = true;
                    this.sheetSelector.appendChild(option);
                });

                this.currentSheetName = res.active_sheet;
                this.currentRawHeaders = res.headers || [];
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
                this.currentSheetName = res.sheet_name;
                this.currentRawHeaders = res.headers || [];
                this.sidebarSearch.value = '';
                this.collapsedNodeIds.clear(); // Reset collapse state on sheet switch
                this.filterAndRenderSidebar();
                if (res.roots) {
                    this.updateUI(res.roots);
                }
                this.showToast(`Switched active sheet to '${sheetName}'.`, "success");
            } else {
                this.showToast(res.error || "Failed to switch sheet.", "error");
            }
        } catch (err) {
            this.showToast("RPC Error switching sheet: " + err, "error");
        }
    },

    filterAndRenderSidebar() {
        const query = this.sidebarSearch.value.trim().toLowerCase();
        const filtered = query
            ? this.currentRawHeaders.filter(h => h.toLowerCase().includes(query))
            : this.currentRawHeaders;

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

        filtered.forEach(headerText => {
            const itemEl = document.createElement('div');
            itemEl.className = 'sidebar-header-item';
            itemEl.dataset.headerLabel = headerText;

            itemEl.innerHTML = `
                <span class="header-title">${this.escapeHtml(headerText)}</span>
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
                this.updateUI(res.roots);
                this.showToast(`Added header node '${headerLabel}' into tree structure.`, "success");
            } else {
                this.showToast(res.error || "Failed to add header node.", "error");
            }
        } catch (err) {
            this.showToast("RPC Error adding header node: " + err, "error");
        }
    },

    // Feature 002: Reconstructed Tree Row 1 Horizontal Export
    async handleExportReorganizedRow1(outputPath) {
        if (!this.currentSheetName) {
            this.showToast("Please import an Excel file session first.", "warning");
            return;
        }

        // Collect leaf path strings from rendered path cards
        const pathElements = this.pathListEl.querySelectorAll('.path-card');
        const leafPaths = Array.from(pathElements).map(el => el.textContent.trim()).filter(Boolean);

        if (leafPaths.length === 0) {
            this.showToast("Tree is empty. Add nodes before exporting.", "warning");
            return;
        }

        try {
            const res = await eel.export_reorganized_row1(this.currentSheetName, leafPaths, outputPath)();
            if (res.success) {
                this.showToast(`Exported ${res.column_count} leaf path columns to '${this.currentSheetName}' in Row 1.`, "success");
            } else {
                this.showToast(res.error || "Failed to export Row 1 paths.", "error");
            }
        } catch (err) {
            this.showToast("RPC Error exporting Row 1: " + err, "error");
        }
    },

    openAddModal(parentId, title) {
        this.activeParentIdForModal = parentId;
        this.modalTitle.textContent = title;
        this.inputNodeName.value = '';
        this.nodeModal.classList.remove('hidden');
        this.inputNodeName.focus();
    },

    closeModal() {
        this.nodeModal.classList.add('hidden');
        this.activeParentIdForModal = null;
    },

    async submitAddModal() {
        const name = this.inputNodeName.value.trim();
        if (!name) {
            this.showToast("Node name cannot be empty.", "warning");
            return;
        }

        try {
            const res = await eel.add_node(this.activeParentIdForModal, name)();
            if (res.success) {
                this.updateUI(res.roots);
                this.closeModal();
                this.showToast(`Node '${name}' created successfully.`, "success");
            } else {
                this.showToast(res.error || "Failed to add node.", "error");
            }
        } catch (err) {
            this.showToast("RPC Error adding node: " + err, "error");
        }
    },

    async handleMoveNode(nodeId, targetId, zone) {
        try {
            const res = await eel.move_node(nodeId, targetId, zone)();
            if (res.success) {
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
