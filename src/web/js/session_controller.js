/**
 * Session Controller (Feature 002, 003, 014, 015, 016, 033)
 * Manages Excel workbook sessions, active sheet switching, dirty tracking, template sync, and pending actions.
 */

const SessionController = {
    app: null,
    currentFileName: null,
    currentSheetName: null,
    catalogSheetName: null,
    cachedAllHeaders: {},
    cachedAllHeadersMeta: {},
    currentRawHeaders: [],
    currentRawHeadersMeta: [],
    currentTemplatePath: null,
    isDirty: false,
    init(app) { this.app = app; },

    async promptOpenAndImportFile() {
        try {
            const res = await eel.open_file_dialog()();
            if (res?.success && !res.cancelled && res.file_path) await this.handleImportExcelFile(res.file_path);
        } catch (err) { if (this.app) this.app.showToast("RPC Error: " + err, "error"); }
    },

    async handleImportExcelFile(filePath) {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        try {
            const res = await eel.import_excel_file(filePath)();
            if (res.success) {
                this.currentFileName = res.file_path.split(/[/\\]/).pop();
                this.currentSheetName = this.catalogSheetName = res.active_sheet;
                this.cachedAllHeaders = res.all_headers || {};
                this.cachedAllHeadersMeta = res.all_headers_meta || {};
                this.currentRawHeaders = res.headers || [];
                this.currentRawHeadersMeta = res.headers_meta || [];
                this.isDirty = false;
                this.updateTemplateBadge(res.template_path);
                this.updateSheetSelectors(res.sheets, res.active_sheet);
                if (window.SidebarController) SidebarController.filterAndRenderSidebar();
                if (this.app) {
                    this.app.updateUI(res.roots);
                    this.app.showToast(t('toast_imported_file', { count: res.headers.length, file: this.currentFileName }), "success");
                }
            } else if (this.app) { this.app.showToast(res.error || t("toast_import_failed"), "error"); }
        } catch (err) { if (this.app) this.app.showToast("RPC Error importing file: " + err, "error"); }
    },

    async handleRefreshExcelSession() {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        if (!this.currentFileName) {
            if (this.app) await this.app.refreshWorkspace();
            return;
        }
        if (this.isDirty) {
            this.pendingAction = { type: 'refresh_session' };
            if (window.ModalManager) ModalManager.promptUnsaved('refresh');
            return;
        }
        try {
            const res = await eel.refresh_excel_session()();
            if (res.success) {
                this.currentSheetName = this.catalogSheetName = res.active_sheet;
                this.cachedAllHeaders = res.all_headers || {};
                this.cachedAllHeadersMeta = res.all_headers_meta || {};
                this.currentRawHeaders = res.headers || [];
                this.currentRawHeadersMeta = res.headers_meta || [];
                this.isDirty = false;
                this.updateTemplateBadge(res.template_path);
                this.updateSheetSelectors(res.sheets, res.active_sheet);
                if (window.SidebarController) SidebarController.filterAndRenderSidebar();
                if (this.app) {
                    this.app.updateUI(res.roots);
                    this.app.showToast(t('toast_refresh_success', { file: this.currentFileName }), "success");
                }
            } else if (this.app) {
                this.app.showToast(res.error || t("toast_refresh_error"), "error");
            }
        } catch (err) {
            if (this.app) this.app.showToast("RPC Error refreshing session: " + err, "error");
        }
    },

    promptSwitchActiveSheet(targetSheet) {
        if (!targetSheet || targetSheet === this.currentSheetName) return;
        if (this.isDirty) {
            this.pendingAction = { type: 'switch_sheet', targetSheet };
            if (window.ModalManager) ModalManager.promptUnsaved('switch_sheet', targetSheet);
        } else {
            this.handleSwitchActiveSheet(targetSheet);
        }
    },

    async handleSwitchActiveSheet(sheetName) {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        try {
            const res = await eel.switch_active_sheet(sheetName)();
            if (res.success) {
                this.currentSheetName = this.catalogSheetName = res.sheet_name;
                this.currentRawHeaders = res.headers || [];
                this.currentRawHeadersMeta = (this.cachedAllHeadersMeta && this.cachedAllHeadersMeta[res.sheet_name]) || [];
                this.isDirty = false;
                this.updateTemplateBadge(res.template_path);
                const s1 = document.getElementById('activeSheetSelector'), s2 = document.getElementById('catalogSheetSelector');
                if (s1) s1.value = res.sheet_name;
                if (s2) s2.value = res.sheet_name;
                if (window.SidebarController) SidebarController.filterAndRenderSidebar();
                if (this.app) this.app.updateUI(res.roots);
            } else if (this.app) {
                this.app.showToast(res.error || t("toast_switch_failed"), "error");
            }
        } catch (err) {
            if (this.app) this.app.showToast("RPC Error switching sheet: " + err, "error");
        }
    },

    handleCatalogSheetChange(sheetName) {
        this.catalogSheetName = sheetName;
        this.currentRawHeaders = this.cachedAllHeaders[sheetName] || [];
        this.currentRawHeadersMeta = this.cachedAllHeadersMeta[sheetName] || [];
        if (window.SidebarController) SidebarController.filterAndRenderSidebar();
    },

    async handleExportTemplate() {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        try {
            const defName = this.currentFileName ? `Шаблон_${this.currentFileName}` : "Шаблон_reorganized_headers_export.xlsx";
            const dRes = await eel.save_file_dialog(defName)();
            if (dRes?.success && !dRes.cancelled && dRes.file_path) {
                const res = await eel.save_template_sync(dRes.file_path)();
                if (res.success) {
                    this.isDirty = false;
                    this.updateTemplateBadge(res.template_path);
                    if (this.app) this.app.showToast(t('toast_template_exported', { template: res.template_path.split(/[/\\]/).pop() }), "success");
                } else if (this.app) {
                    this.app.showToast(res.error || t("toast_template_failed"), "error");
                }
            }
        } catch (err) {
            if (this.app) this.app.showToast("RPC Error saving template: " + err, "error");
        }
    },

    async executePendingAction(shouldSaveFirst) {
        const action = this.pendingAction;
        this.pendingAction = null;
        this.isDirty = false;
        if (shouldSaveFirst) {
            try {
                const res = await eel.save_template_sync(this.currentTemplatePath)();
                if (res.success) {
                    this.updateTemplateBadge(res.template_path);
                }
            } catch (err) {
                if (this.app) this.app.showToast("RPC Error saving template: " + err, "error");
            }
        }
        if (!action) return;
        if (action.type === 'switch_sheet') await this.handleSwitchActiveSheet(action.targetSheet);
        else if (action.type === 'import_file') await this.promptOpenAndImportFile();
        else if (action.type === 'refresh_session') {
            this.isDirty = false;
            await this.handleRefreshExcelSession();
        }
    },

    updateTemplateBadge(path) {
        this.currentTemplatePath = path || null;
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        const badge = document.getElementById('templateStatusBadge');
        if (badge) {
            const base = this.currentTemplatePath ? this.currentTemplatePath.split(/[/\\]/).pop() : null;
            badge.textContent = base ? `${t('template_prefix')}: ${base} (Synced)` : `${t('template_prefix')}: ${t('template_none')}`;
            badge.title = base ? `${t('template_status_title')}: ${this.currentTemplatePath}` : t('template_status_title');
        }
    },

    updateSheetSelectors(sheets, activeSheet) {
        const s1 = document.getElementById('activeSheetSelector'), s2 = document.getElementById('catalogSheetSelector');
        const searchInput = document.getElementById('sidebarSearch');
        if (!sheets || sheets.length === 0) {
            if (s1) s1.disabled = true;
            if (s2) s2.disabled = true;
            if (searchInput) searchInput.disabled = true;
            return;
        }
        if (s1) s1.disabled = false;
        if (s2) s2.disabled = false;
        if (searchInput) searchInput.disabled = false;
        const opts = sheets.map(s => `<option value="${this.escapeHtml(s)}">${this.escapeHtml(s)}</option>`).join('');
        if (s1) { s1.innerHTML = opts; s1.value = activeSheet; }
        if (s2) { s2.innerHTML = opts; s2.value = activeSheet; }
    },

    escapeHtml(str) { return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
};

window.SessionController = SessionController;
