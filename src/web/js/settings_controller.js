/**
 * Settings Controller (Feature 026, 033)
 * Manages Path Delimiter and Default Data Type Settings Modal and RPC synchronization.
 */

const SettingsController = {
    app: null,

    init(app) {
        this.app = app;
        this.bindDOM();
        this.bindEvents();
    },

    bindDOM() {
        this.settingsModal = document.getElementById('settingsModal');
        this.settingsModalClose = document.getElementById('settingsModalClose');
        this.inputSettingDelimiter = document.getElementById('inputSettingDelimiter');
        this.selectSettingDefaultType = document.getElementById('selectSettingDefaultType');
        this.btnSettingsReset = document.getElementById('btnSettingsReset');
        this.btnSettingsCancel = document.getElementById('btnSettingsCancel');
        this.btnSettingsSave = document.getElementById('btnSettingsSave');
    },

    bindEvents() {
        if (this.settingsModalClose) this.settingsModalClose.addEventListener('click', () => this.closeSettingsModal());
        if (this.btnSettingsCancel) this.btnSettingsCancel.addEventListener('click', () => this.closeSettingsModal());
        if (this.btnSettingsReset) this.btnSettingsReset.addEventListener('click', () => this.resetSettingsModal());
        if (this.btnSettingsSave) this.btnSettingsSave.addEventListener('click', () => this.saveSettingsModal());
    },

    openSettingsModal() {
        if (!this.settingsModal) return;
        const current = (this.app && this.app.settings) ? this.app.settings : { delimiter: '\\', default_data_type: 'Text' };
        if (this.inputSettingDelimiter) this.inputSettingDelimiter.value = current.delimiter || '\\';
        if (this.selectSettingDefaultType) this.selectSettingDefaultType.value = current.default_data_type || 'Text';
        this.settingsModal.classList.remove('hidden');
    },

    closeSettingsModal() {
        if (this.settingsModal) this.settingsModal.classList.add('hidden');
    },

    async saveSettingsModal() {
        const delim = this.inputSettingDelimiter ? this.inputSettingDelimiter.value.trim() : '\\';
        const defType = this.selectSettingDefaultType ? this.selectSettingDefaultType.value : 'Text';
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        try {
            const res = await eel.update_settings(delim, defType)();
            if (res.success) {
                if (this.app) {
                    this.app.settings = res.settings;
                    this.app.updateUI(res.roots);
                    this.app.showToast(t("toast_settings_saved"), "success");
                }
            } else if (this.app) { this.app.showToast(res.error, "error"); }
        } catch (err) { if (this.app) this.app.showToast("RPC Error: " + err, "error"); }
        this.closeSettingsModal();
    },

    async resetSettingsModal() {
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        try {
            const res = await eel.reset_settings()();
            if (res.success) {
                if (this.app) {
                    this.app.settings = res.settings;
                    this.app.updateUI(res.roots);
                    this.app.showToast(t("toast_settings_reset"), "info");
                }
            }
        } catch (err) { if (this.app) this.app.showToast("RPC Error: " + err, "error"); }
        this.closeSettingsModal();
    }
};

window.SettingsController = SettingsController;
