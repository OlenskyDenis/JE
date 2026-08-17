/**
 * Sidebar Controller (Feature 002, 013, 015, 033)
 * Encapsulates Sidebar Tabs, Sheet Dropdowns, Search Filters, Drag-to-Resize, and Collapsible Strip.
 */

const SidebarController = {
    app: null,

    init(app) {
        this.app = app;
        this.bindDOM();
        this.bindEvents();
        this.initResizer();
        this.switchTab(this.sidebarTabSelector ? this.sidebarTabSelector.value : 'catalog');
    },

    bindDOM() {
        this.unifiedSidebar = document.getElementById('unifiedSidebar');
        this.sidebarResizer = document.getElementById('sidebarResizer');
        this.btnToggleSidebarCollapse = document.getElementById('btnToggleSidebarCollapse');
        this.btnExpandSidebarStrip = document.getElementById('btnExpandSidebarStrip');
        this.sidebarCollapsedStrip = document.getElementById('sidebarCollapsedStrip');
        this.sidebarTabSelector = document.getElementById('sidebarTabSelector');
        this.tabContentCatalog = document.getElementById('tabContentCatalog');
        this.tabContentPaths = document.getElementById('tabContentPaths');
        this.activeSheetSelector = document.getElementById('activeSheetSelector');
        this.catalogSheetSelector = document.getElementById('catalogSheetSelector');
        this.sidebarSearch = document.getElementById('sidebarSearch');
        this.sidebarHeaderList = document.getElementById('sidebarHeaderList');
        this.sidebarEmptyState = document.getElementById('sidebarEmptyState');
        this.headerCountBadge = document.getElementById('headerCountBadge');
        this.pathCountBadge = document.getElementById('pathCountBadge');
        this.pathListEl = document.getElementById('pathList');
    },

    bindEvents() {
        if (this.sidebarTabSelector) {
            this.sidebarTabSelector.addEventListener('change', () => this.switchTab(this.sidebarTabSelector.value));
        }
        if (this.btnToggleSidebarCollapse) {
            this.btnToggleSidebarCollapse.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleCollapse(true);
            });
        }
        if (this.btnExpandSidebarStrip) {
            this.btnExpandSidebarStrip.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleCollapse(false);
            });
        }
        if (this.sidebarCollapsedStrip) {
            this.sidebarCollapsedStrip.addEventListener('click', () => this.toggleCollapse(false));
        }
        if (this.sidebarSearch) {
            this.sidebarSearch.addEventListener('input', () => this.filterAndRenderSidebar());
        }
        if (this.activeSheetSelector) {
            this.activeSheetSelector.addEventListener('change', (e) => {
                if (window.SessionController) SessionController.promptSwitchActiveSheet(e.target.value);
            });
        }
        if (this.catalogSheetSelector) {
            this.catalogSheetSelector.addEventListener('change', (e) => {
                if (window.SessionController) SessionController.handleCatalogSheetChange(e.target.value);
            });
        }
        if (this.sidebarHeaderList) {
            this.sidebarHeaderList.addEventListener('dragstart', (e) => {
                const item = e.target.closest('.sidebar-header-item');
                if (item && window.DragDropHandler) {
                    const headerLabel = item.getAttribute('data-header-name') || item.getAttribute('data-header-label');
                    const dataType = item.getAttribute('data-data-type') || 'Text';
                    DragDropHandler.activeDragPayload = { isNew: true, label: headerLabel, name: headerLabel, dataType };
                    e.dataTransfer.setData('application/json', JSON.stringify(DragDropHandler.activeDragPayload));
                    e.dataTransfer.setData('text/plain', headerLabel);
                    e.dataTransfer.setData('source', 'sidebar_catalog');
                    e.dataTransfer.effectAllowed = 'copy';
                }
            });
            this.sidebarHeaderList.addEventListener('dragend', () => {
                if (window.DragDropHandler) DragDropHandler.handleDragEnd();
            });
        }
    },

    switchTab(tabName) {
        if (this.sidebarTabSelector && this.sidebarTabSelector.value !== tabName) {
            this.sidebarTabSelector.value = tabName;
        }
        if (tabName === 'catalog') {
            if (this.tabContentCatalog) {
                this.tabContentCatalog.classList.remove('hidden');
                this.tabContentCatalog.classList.add('active');
            }
            if (this.tabContentPaths) {
                this.tabContentPaths.classList.add('hidden');
                this.tabContentPaths.classList.remove('active');
            }
            if (this.headerCountBadge) this.headerCountBadge.classList.remove('hidden');
            if (this.pathCountBadge) this.pathCountBadge.classList.add('hidden');
            this.filterAndRenderSidebar();
        } else if (tabName === 'paths') {
            if (this.tabContentCatalog) {
                this.tabContentCatalog.classList.add('hidden');
                this.tabContentCatalog.classList.remove('active');
            }
            if (this.tabContentPaths) {
                this.tabContentPaths.classList.remove('hidden');
                this.tabContentPaths.classList.add('active');
            }
            if (this.headerCountBadge) this.headerCountBadge.classList.add('hidden');
            if (this.pathCountBadge) this.pathCountBadge.classList.remove('hidden');
        }
    },

    toggleCollapse(forceCollapse) {
        if (!this.unifiedSidebar) return;
        const isCollapsed = forceCollapse !== undefined ? forceCollapse : !this.unifiedSidebar.classList.contains('sidebar-collapsed');
        if (isCollapsed) {
            this.unifiedSidebar.classList.add('sidebar-collapsed');
            localStorage.setItem('je_sidebar_collapsed', 'true');
        } else {
            this.unifiedSidebar.classList.remove('sidebar-collapsed');
            localStorage.setItem('je_sidebar_collapsed', 'false');
        }
    },

    initResizer() {
        if (!this.sidebarResizer || !this.unifiedSidebar) return;
        let isDragging = false, startX = 0, startWidth = 340;
        const onPointerDown = (e) => {
            if (this.unifiedSidebar.classList.contains('sidebar-collapsed')) return;
            isDragging = true;
            startX = e.clientX;
            startWidth = this.unifiedSidebar.getBoundingClientRect().width;
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
        };
        const onPointerMove = (e) => {
            if (!isDragging) return;
            const newWidth = Math.min(600, Math.max(220, startWidth - (e.clientX - startX)));
            this.unifiedSidebar.style.width = `${newWidth}px`;
        };
        const onPointerUp = () => {
            if (!isDragging) return;
            isDragging = false;
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        };
        this.sidebarResizer.addEventListener('pointerdown', onPointerDown);
        window.addEventListener('pointermove', onPointerMove);
        window.addEventListener('pointerup', onPointerUp);
        this.sidebarResizer.addEventListener('dblclick', () => {
            this.unifiedSidebar.style.width = '340px';
            localStorage.setItem('je_sidebar_width', '340');
        });
        const savedWidth = localStorage.getItem('je_sidebar_width');
        if (savedWidth) this.unifiedSidebar.style.width = `${savedWidth}px`;
        if (localStorage.getItem('je_sidebar_collapsed') === 'true') this.toggleCollapse(true);
    },

    filterAndRenderSidebar() {
        if (!this.sidebarHeaderList) return;
        const query = (this.sidebarSearch ? this.sidebarSearch.value : '').toLowerCase().trim();
        const headers = window.SessionController ? SessionController.currentRawHeaders : [];
        const meta = window.SessionController ? SessionController.currentRawHeadersMeta : [];
        const typeMap = {};
        meta.forEach(item => { if (item.name) typeMap[item.name] = item.type; });
        const filtered = headers.filter(h => h.toLowerCase().includes(query));
        if (this.headerCountBadge) this.headerCountBadge.textContent = filtered.length;
        if (filtered.length === 0) {
            this.sidebarHeaderList.innerHTML = '';
            if (this.sidebarEmptyState) this.sidebarEmptyState.classList.remove('hidden');
            this.sidebarHeaderList.classList.add('hidden');
            return;
        }
        if (this.sidebarEmptyState) this.sidebarEmptyState.classList.add('hidden');
        this.sidebarHeaderList.classList.remove('hidden');
        this.sidebarHeaderList.innerHTML = filtered.map(header => {
            const dtype = typeMap[header] || 'Text';
            const badgeLabel = window.I18n ? I18n.getTypeLabel(dtype) : dtype;
            return `
                <div class="sidebar-header-item" draggable="true" data-header-name="${this.escapeHtml(header)}" data-header-label="${this.escapeHtml(header)}" data-data-type="${this.escapeHtml(dtype)}">
                    <span class="sidebar-item-icon">📄</span>
                    <span class="sidebar-item-label header-title" title="${this.escapeHtml(header)}">${this.escapeHtml(header)}</span>
                    <span class="type-badge" title="${this.escapeHtml(dtype)}">${this.escapeHtml(badgeLabel)}</span>
                </div>
            `;
        }).join('');
    },

    escapeHtml(str) { return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
};

window.SidebarController = SidebarController;
