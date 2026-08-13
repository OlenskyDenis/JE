/**
 * Main Application Module connecting Eel RPC backend with HTML5 Frontend.
 */

document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

const App = {
    activeParentIdForModal: null,

    async init() {
        this.bindDOM();
        this.bindEvents();
        DragDropHandler.init(
            document.getElementById('treeView'),
            (nodeId, targetId, zone) => this.handleMoveNode(nodeId, targetId, zone),
            (msg, type) => this.showToast(msg, type)
        );

        // Initial fetch of workspace tree
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
        this.excelFileInput = document.getElementById('excelFileInput');
    },

    bindEvents() {
        document.getElementById('btnAddRoot').addEventListener('click', () => this.openAddModal(null, "Add Root Node"));
        document.getElementById('btnRefresh').addEventListener('click', () => this.refreshWorkspace());

        document.getElementById('btnImportExcel').addEventListener('click', () => {
            // Trigger file input dialog or prompt for path
            const path = prompt("Enter the absolute file path of the Excel (.xlsx) file to import:");
            if (path && path.trim()) {
                this.handleImportExcel(path.trim());
            }
        });

        document.getElementById('btnExportExcel').addEventListener('click', () => {
            const defaultName = "hierarchy_export.xlsx";
            const path = prompt("Enter output Excel (.xlsx) file path to save:", defaultName);
            if (path && path.trim()) {
                this.handleExportExcel(path.trim());
            }
        });

        // Delegate click events on tree view
        this.treeViewEl.addEventListener('click', (e) => {
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
            console.warn("Eel backend not connected. Using local mode.");
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
        TreeRenderer.renderTree(roots, this.treeViewEl);
        TreeRenderer.renderPaths(roots, this.pathListEl);

        let totalNodes = 0;
        function countNodes(node) {
            totalNodes++;
            if (node.children) node.children.forEach(countNodes);
        }
        if (roots) roots.forEach(countNodes);

        this.nodeCountBadge.textContent = `${totalNodes} Nodes`;
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

        const selectedType = document.querySelector('input[name="nodeType"]:checked').value;
        const isContainer = selectedType === 'container';

        try {
            const res = await eel.add_node(this.activeParentIdForModal, name, isContainer)();
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

    async handleImportExcel(filePath) {
        try {
            const res = await eel.import_excel(filePath)();
            if (res.success) {
                this.updateUI(res.roots);
                this.showToast(`Successfully imported Excel hierarchy (${res.imported_count} top-level roots).`, "success");
            } else {
                this.showToast(res.error || "Failed to import Excel file.", "error");
            }
        } catch (err) {
            this.showToast("RPC Error importing Excel: " + err, "error");
        }
    },

    async handleExportExcel(filePath) {
        try {
            const res = await eel.export_excel(filePath)();
            if (res.success) {
                this.showToast(`Successfully exported ${res.exported_paths} leaf paths to Excel file.`, "success");
            } else {
                this.showToast(res.error || "Failed to export Excel file.", "error");
            }
        } catch (err) {
            this.showToast("RPC Error exporting Excel: " + err, "error");
        }
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
