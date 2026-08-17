/**
 * Main Application Orchestrator (Features 001-033)
 * Coordinates SessionController, ModalManager, SidebarController, ViewModeManager, and DragDropHandler.
 */

document.addEventListener('DOMContentLoaded', () => { App.init(); });

const App = {
    collapsedNodeIds: new Set(),
    currentRoots: [],
    settings: { delimiter: '\\', default_data_type: 'Text' },

    get currentRawHeaders() { return window.SessionController?.currentRawHeaders || []; },
    set currentRawHeaders(v) { if (window.SessionController) SessionController.currentRawHeaders = v; },
    get currentRawHeadersMeta() { return window.SessionController?.currentRawHeadersMeta || []; },
    set currentRawHeadersMeta(v) { if (window.SessionController) SessionController.currentRawHeadersMeta = v; },
    get currentFileName() { return window.SessionController?.currentFileName || null; },
    set currentFileName(v) { if (window.SessionController) SessionController.currentFileName = v; },
    get currentFilePath() { return window.SessionController?.currentTemplatePath || null; },
    set currentFilePath(v) { if (window.SessionController) SessionController.currentTemplatePath = v; },
    get currentSheetName() { return window.SessionController?.currentSheetName || null; },
    set currentSheetName(v) { if (window.SessionController) SessionController.currentSheetName = v; },
    get catalogSheetName() { return window.SessionController?.catalogSheetName || null; },
    set catalogSheetName(v) { if (window.SessionController) SessionController.catalogSheetName = v; },
    get isDirty() { return window.SessionController?.isDirty || false; },
    set isDirty(v) { if (window.SessionController) SessionController.isDirty = v; },
    get currentTemplatePath() { return window.SessionController?.currentTemplatePath || null; },
    set currentTemplatePath(v) { if (window.SessionController) SessionController.currentTemplatePath = v; },
    get cachedAllHeaders() { return window.SessionController?.cachedAllHeaders || {}; },
    set cachedAllHeaders(v) { if (window.SessionController) SessionController.cachedAllHeaders = v; },
    get cachedAllHeadersMeta() { return window.SessionController?.cachedAllHeadersMeta || {}; },
    set cachedAllHeadersMeta(v) { if (window.SessionController) SessionController.cachedAllHeadersMeta = v; },
    get activeSheetSelector() { return document.getElementById('activeSheetSelector'); },
    get catalogSheetSelector() { return document.getElementById('catalogSheetSelector'); },

    async init() {
        this.bindDOM();
        this.bindGlobalEvents();
        if (window.SessionController) SessionController.init(this);
        if (window.ModalManager) ModalManager.init(this);
        if (window.SidebarController) SidebarController.init(this);
        if (window.ViewModeManager) ViewModeManager.init(this);
        if (window.SettingsController) SettingsController.init(this);
        if (window.I18n) {
            I18n.init();
            I18n.onLanguageChanged(() => {
                if (window.SessionController) SessionController.updateTemplateBadge(SessionController.currentTemplatePath);
                this.updateUI(this.currentRoots);
                if (window.SidebarController) SidebarController.filterAndRenderSidebar();
            });
        }
        DragDropHandler.init(document.getElementById('treeView'), (p, tid, z) => this.handleDropPayload(p, tid, z), (msg, t) => this.showToast(msg, t));
        await this.loadInitialSettings();
        await this.refreshWorkspace();
    },

    bindDOM() {
        this.nodeCountBadge = document.getElementById('nodeCountBadge');
        this.toastContainer = document.getElementById('toastContainer');
        this.pathListEl = document.getElementById('pathList');
        this.pathCountBadge = document.getElementById('pathCountBadge');
    },
    bindGlobalEvents() {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        const lUk = document.getElementById('langBtnUk'), lEn = document.getElementById('langBtnEn');
        if (lUk) lUk.addEventListener('click', () => window.I18n && I18n.setLanguage('uk'));
        if (lEn) lEn.addEventListener('click', () => window.I18n && I18n.setLanguage('en'));
        const cEmpty = document.getElementById('btnCreateRootEmpty'), aRoot = document.getElementById('btnAddRootHeader');
        if (cEmpty) cEmpty.addEventListener('click', () => window.ModalManager && ModalManager.openAddModal(null, t("modal_create_title")));
        if (aRoot) aRoot.addEventListener('click', () => window.ModalManager && ModalManager.openAddModal(null, t("modal_create_title")));
        document.getElementById('btnRefresh').addEventListener('click', () => window.SessionController && SessionController.handleRefreshExcelSession());
        const exp = document.getElementById('btnExpandAll'), col = document.getElementById('btnCollapseAll');
        if (exp) exp.addEventListener('click', () => this.expandAll());
        if (col) col.addEventListener('click', () => this.collapseAll());
        const setBtn = document.getElementById('btnSettings');
        if (setBtn) setBtn.addEventListener('click', () => window.SettingsController && SettingsController.openSettingsModal());
        document.getElementById('btnImportExcel').addEventListener('click', async () => {
            if (window.SessionController && SessionController.isDirty) {
                SessionController.pendingAction = { type: 'import_file' };
                if (window.ModalManager) ModalManager.promptUnsaved('import');
            } else if (window.SessionController) {
                await SessionController.promptOpenAndImportFile();
            }
        });
        document.getElementById('btnExportExcel').addEventListener('click', () => {
            if (window.SessionController) SessionController.handleExportTemplate();
        });
    },
    filterAndRenderSidebar() { if (window.SidebarController) SidebarController.filterAndRenderSidebar(); },
    updateTemplateBadge(path) { if (window.SessionController) SessionController.updateTemplateBadge(path); },
    switchTab(tab) { if (window.SidebarController) SidebarController.switchTab(tab); },
    switchViewMode(mode) { if (window.ViewModeManager) ViewModeManager.switchViewMode(mode); },

    async handleNodeDelete(nodeId) {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        if (confirm(t("confirm_delete_node"))) {
            try {
                const res = await eel.delete_node(nodeId)();
                if (res.success) {
                    if (window.SessionController) SessionController.isDirty = true;
                    this.updateUI(res.roots);
                    this.showToast(t("toast_node_deleted"), "info");
                }
            } catch (err) { this.showToast("RPC Error: " + err, "error"); }
        }
    },

    async handleDropPayload(payload, targetId, zone) {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        try {
            if (!payload.isNew && (payload.id || payload.type === 'existing_node')) {
                const res = await eel.move_node(payload.id, targetId, zone)();
                if (res.success) {
                    if (window.SessionController) SessionController.isDirty = true;
                    this.updateUI(res.roots);
                } else if (res.rejection_reason) {
                    this.showToast(res.rejection_reason || t("toast_move_rejected"), "warning");
                }
            } else if (payload.isNew || payload.type === 'new_sidebar_header') {
                const headerName = payload.label || payload.name;
                const dtype = payload.dataType || this.settings.default_data_type || 'Text';
                const res = await eel.add_node(null, headerName, true, targetId, zone, dtype)();
                if (res.success) {
                    if (window.SessionController) SessionController.isDirty = true;
                    this.updateUI(res.roots);
                }
            }
        } catch (err) { this.showToast("RPC Error in drop: " + err, "error"); }
    },

    async loadInitialSettings() {
        try {
            const res = await eel.get_settings()();
            if (res.success && res.settings) this.settings = res.settings;
        } catch (err) { console.error("Error settings:", err); }
    },

    async refreshWorkspace() {
        try {
            const res = await eel.get_settings()();
            if (res.success && res.settings) this.settings = res.settings;
        } catch (err) {}
        this.updateUI(this.currentRoots);
    },

    updateUI(roots) {
        this.currentRoots = roots || [];
        if (window.ViewModeManager) ViewModeManager.renderCurrentView(this.currentRoots);
        this.renderPaths(this.currentRoots);
        if (this.nodeCountBadge) this.nodeCountBadge.textContent = this.countTotalNodes(this.currentRoots);
    },

    renderPaths(roots) {
        if (!this.pathListEl) return;
        const paths = [];
        const traverse = (node) => {
            if (!node.children || node.children.length === 0) paths.push(node.absolute_path || node.name);
            else node.children.forEach(traverse);
        };
        (roots || []).forEach(traverse);
        if (this.pathCountBadge) this.pathCountBadge.textContent = paths.length;
        this.pathListEl.innerHTML = paths.length === 0 ? '<li class="path-item-empty" data-i18n="empty_no_paths">No leaf paths generated yet.</li>' : paths.map(p => `<li class="path-item">${this.escapeHtml(p)}</li>`).join('');
    },

    countTotalNodes(roots) {
        let count = 0;
        const traverse = (n) => { count += 1; (n.children || []).forEach(traverse); };
        (roots || []).forEach(traverse);
        return count;
    },

    expandAll() { this.collapsedNodeIds.clear(); this.updateUI(this.currentRoots); },
    collapseAll() {
        const traverse = (n) => {
            if (n.children && n.children.length > 0) { this.collapsedNodeIds.add(n.id); n.children.forEach(traverse); }
        };
        (this.currentRoots || []).forEach(traverse);
        this.updateUI(this.currentRoots);
    },
    toggleNodeCollapse(nodeId) {
        if (!nodeId) return;
        if (this.collapsedNodeIds.has(nodeId)) this.collapsedNodeIds.delete(nodeId);
        else this.collapsedNodeIds.add(nodeId);
        this.updateUI(this.currentRoots);
    },

    showToast(message, type = 'info') {
        if (!this.toastContainer) return;
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        this.toastContainer.appendChild(toast);
        setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 250); }, 3000);
    },

    escapeHtml(str) { return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
};

window.App = App;
