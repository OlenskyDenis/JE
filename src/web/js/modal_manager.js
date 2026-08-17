/**
 * Modal Manager (Feature 010, 015, 019, 020, 026, 033)
 * Encapsulates Node Add/Edit Modals and Unsaved Changes Confirmation Dialogs.
 */

const ModalManager = {
    app: null,
    modalMode: 'create',
    activeParentIdForModal: null,
    activeNodeIdForEdit: null,
    batchNodeIdsForEdit: [],

    init(app) {
        this.app = app;
        this.bindDOM();
        this.bindEvents();
    },

    bindDOM() {
        this.nodeModal = document.getElementById('nodeModal');
        this.modalTitle = document.getElementById('modalTitle');
        this.inputNodeName = document.getElementById('inputNodeName');
        this.groupNodeType = document.getElementById('groupNodeType');
        this.selectNodeType = document.getElementById('selectNodeType');
        this.folderTypeHint = document.getElementById('folderTypeHint');
        this.modalBatchNotice = document.getElementById('modalBatchNotice');
        this.modalBatchNoticeText = document.getElementById('modalBatchNoticeText');
        this.btnModalSubmit = document.getElementById('btnModalSubmit');
        this.btnModalCancel = document.getElementById('btnModalCancel');
        this.modalClose = document.getElementById('modalClose');

        this.unsavedModal = document.getElementById('unsavedModal');
        this.unsavedModalMessage = document.getElementById('unsavedModalMessage');
        this.unsavedModalClose = document.getElementById('unsavedModalClose');
        this.btnUnsavedCancel = document.getElementById('btnUnsavedCancel');
        this.btnUnsavedDiscard = document.getElementById('btnUnsavedDiscard');
        this.btnUnsavedSave = document.getElementById('btnUnsavedSave');
    },

    bindEvents() {
        const closeUnsavedModal = () => {
            if (this.unsavedModal) this.unsavedModal.classList.add('hidden');
        };
        const cancelUnsaved = () => {
            closeUnsavedModal();
            if (window.SessionController) {
                SessionController.pendingAction = null;
                const sel = document.getElementById('activeSheetSelector');
                if (sel && SessionController.currentSheetName) sel.value = SessionController.currentSheetName;
            }
        };
        if (this.modalClose) this.modalClose.addEventListener('click', () => this.closeModal());
        if (this.btnModalCancel) this.btnModalCancel.addEventListener('click', () => this.closeModal());
        if (this.btnModalSubmit) this.btnModalSubmit.addEventListener('click', () => this.submitModal());
        if (this.inputNodeName) {
            this.inputNodeName.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') this.submitModal();
                if (e.key === 'Escape') this.closeModal();
            });
        }
        if (this.unsavedModalClose) this.unsavedModalClose.addEventListener('click', cancelUnsaved);
        if (this.btnUnsavedCancel) this.btnUnsavedCancel.addEventListener('click', cancelUnsaved);
        if (this.btnUnsavedDiscard) {
            this.btnUnsavedDiscard.addEventListener('click', async () => {
                closeUnsavedModal();
                if (window.SessionController) await SessionController.executePendingAction(false);
            });
        }
        if (this.btnUnsavedSave) {
            this.btnUnsavedSave.addEventListener('click', async () => {
                closeUnsavedModal();
                if (window.SessionController) await SessionController.executePendingAction(true);
            });
        }
    },

    openAddModal(parentId, title) {
        this.modalMode = 'create';
        this.activeParentIdForModal = parentId;
        this.activeNodeIdForEdit = null;
        this.batchNodeIdsForEdit = [];
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        this.modalTitle.textContent = title || t("modal_create_title");
        this.btnModalSubmit.textContent = t("modal_create_btn");
        this.inputNodeName.value = '';
        if (this.modalBatchNotice) this.modalBatchNotice.classList.add('hidden');
        if (this.groupNodeType) {
            this.groupNodeType.classList.remove('hidden');
            if (this.selectNodeType) {
                this.selectNodeType.disabled = false;
                this.selectNodeType.value = (this.app?.settings?.default_data_type) || 'Text';
            }
            if (this.folderTypeHint) this.folderTypeHint.classList.add('hidden');
        }
        this.nodeModal.classList.remove('hidden');
        setTimeout(() => this.inputNodeName.focus(), 50);
    },

    openEditModal(nodeId, currentName, currentType = 'Text', isFolder = false, batchCount = 1, batchNodeIds = []) {
        this.modalMode = 'edit';
        this.activeNodeIdForEdit = nodeId;
        this.batchNodeIdsForEdit = batchNodeIds && batchNodeIds.length > 0 ? batchNodeIds : [nodeId];
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        this.modalTitle.textContent = t("modal_edit_title");
        this.btnModalSubmit.textContent = t("modal_edit_btn");
        this.inputNodeName.value = currentName;
        if (this.modalBatchNotice) {
            this.modalBatchNotice.classList.toggle('hidden', batchCount <= 1);
            if (this.modalBatchNoticeText && batchCount > 1) {
                this.modalBatchNoticeText.textContent = t("modal_batch_edit_notice", { count: batchCount });
            }
        }
        if (this.groupNodeType) {
            this.groupNodeType.classList.remove('hidden');
            if (this.selectNodeType) {
                this.selectNodeType.value = currentType || 'Text';
                this.selectNodeType.disabled = isFolder;
            }
            if (this.folderTypeHint) this.folderTypeHint.classList.toggle('hidden', !isFolder);
        }
        this.nodeModal.classList.remove('hidden');
        setTimeout(() => { this.inputNodeName.focus(); this.inputNodeName.select(); }, 50);
    },

    closeModal() {
        if (this.modalBatchNotice) this.modalBatchNotice.classList.add('hidden');
        if (this.nodeModal) this.nodeModal.classList.add('hidden');
        this.modalMode = 'create';
        this.activeParentIdForModal = null;
        this.activeNodeIdForEdit = null;
        this.batchNodeIdsForEdit = [];
    },

    async submitModal() {
        const name = this.inputNodeName.value.trim();
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        if (!name) {
            if (this.app) this.app.showToast(t("toast_name_required"), "warning");
            return;
        }
        if (this.modalMode === 'edit') {
            const selectedType = this.selectNodeType && !this.selectNodeType.disabled ? this.selectNodeType.value : null;
            try {
                let lastRoots = this.app.currentRoots;
                for (const nid of this.batchNodeIdsForEdit) {
                    const res = await eel.update_node(nid, name, selectedType)();
                    if (res.success) {
                        lastRoots = res.roots;
                        if (window.SessionController) SessionController.isDirty = true;
                    } else if (this.app) { this.app.showToast(res.error, "error"); }
                }
                if (this.app) {
                    this.app.updateUI(lastRoots);
                    this.app.showToast(t("toast_node_updated", { name }), "success");
                }
            } catch (err) { if (this.app) this.app.showToast("RPC Error: " + err, "error"); }
        } else {
            try {
                const selectedType = this.selectNodeType ? this.selectNodeType.value : ((this.app?.settings?.default_data_type) || 'Text');
                const res = await eel.add_node(this.activeParentIdForModal, name, true, null, null, selectedType)();
                if (res.success) {
                    if (window.SessionController) SessionController.isDirty = true;
                    if (this.app) {
                        this.app.updateUI(res.roots);
                        this.app.showToast(t("toast_node_created", { name }), "success");
                    }
                } else if (this.app) { this.app.showToast(res.error, "error"); }
            } catch (err) { if (this.app) this.app.showToast("RPC Error: " + err, "error"); }
        }
        this.closeModal();
    },

    promptUnsaved(actionType, targetSheet = null) {
        if (!this.unsavedModal) return;
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        const esc = (s) => (this.app ? this.app.escapeHtml(s) : s);
        const tpl = window.SessionController ? SessionController.currentTemplatePath : null;

        if (actionType === 'import') {
            this.unsavedModalMessage.innerHTML = tpl ? t('unsaved_msg_import_update', { template: esc(tpl.split(/[/\\]/).pop()) }) : t('unsaved_msg_import_save');
            this.btnUnsavedSave.textContent = tpl ? t("unsaved_btn_update_import") : t("unsaved_btn_save_import");
            this.btnUnsavedDiscard.textContent = t("unsaved_btn_discard_import");
        } else if (actionType === 'switch_sheet') {
            const cur = (window.SessionController && SessionController.currentSheetName) || '';
            this.unsavedModalMessage.innerHTML = tpl ? t('unsaved_msg_switch_update', { template: esc(tpl.split(/[/\\]/).pop()), current: esc(cur), target: esc(targetSheet) }) : t('unsaved_msg_switch_save', { current: esc(cur), target: esc(targetSheet) });
            this.btnUnsavedSave.textContent = tpl ? t("unsaved_btn_update_switch") : t("unsaved_btn_save_switch");
            this.btnUnsavedDiscard.textContent = t("unsaved_btn_discard_switch");
        } else if (actionType === 'refresh') {
            this.unsavedModalMessage.innerHTML = tpl ? t('unsaved_msg_refresh_update', { template: esc(tpl.split(/[/\\]/).pop()) }) : t('unsaved_msg_refresh_save');
            this.btnUnsavedSave.textContent = tpl ? t("unsaved_btn_update_refresh") : t("unsaved_btn_save_refresh");
            this.btnUnsavedDiscard.textContent = t("unsaved_btn_discard_refresh");
        }
        this.unsavedModal.classList.remove('hidden');
    }
};

window.ModalManager = ModalManager;
