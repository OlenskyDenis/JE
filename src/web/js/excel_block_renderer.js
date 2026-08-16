/**
 * Excel Block Matrix Renderer (Feature 027)
 * Translates multi-root WorkspaceForest trees into human-readable,
 * multi-tier spreadsheet block matrix tables mimicking Excel merged header cells.
 */

const ExcelBlockRenderer = {
    escapeHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    },

    /**
     * Calculates maximum depth across all trees in the forest (1-indexed).
     * Returns 0 if forest is empty.
     */
    getMaxDepth(roots) {
        if (!roots || !Array.isArray(roots) || roots.length === 0) return 0;

        function computeDepth(node) {
            if (!node || !node.children || node.children.length === 0) return 1;
            return 1 + Math.max(...node.children.map(computeDepth));
        }

        return Math.max(...roots.map(computeDepth));
    },

    /**
     * Calculates total leaf column width of a node or subtree.
     */
    getLeafCount(node) {
        if (!node) return 0;
        if (!node.children || node.children.length === 0) return 1;
        return node.children.reduce((acc, ch) => acc + this.getLeafCount(ch), 0);
    },

    /**
     * Converts a 0-based column index to an Excel column coordinate string (e.g. 0 -> 'A', 25 -> 'Z', 26 -> 'AA').
     */
    getExcelColumnLabel(colIndex) {
        let columnName = '';
        let num = colIndex + 1; // 1-indexed
        while (num > 0) {
            const rem = (num - 1) % 26;
            columnName = String.fromCharCode(65 + rem) + columnName;
            num = Math.floor((num - 1) / 26);
        }
        return columnName;
    },

    /**
     * Builds the 2D multi-tier matrix layout metadata.
     */
    buildMatrixLayout(roots) {
        if (!roots || !Array.isArray(roots) || roots.length === 0) {
            return {
                maxDepth: 0,
                totalColumns: 0,
                columnLabels: [],
                tierRows: []
            };
        }

        const maxDepth = this.getMaxDepth(roots);
        const totalColumns = roots.reduce((acc, r) => acc + this.getLeafCount(r), 0);
        const columnLabels = Array.from({ length: totalColumns }, (_, i) => this.getExcelColumnLabel(i));
        const tierRows = Array.from({ length: maxDepth }, () => []);

        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);

        const traverse = (node, level) => {
            const isLeaf = !node.children || node.children.length === 0;
            const colSpan = this.getLeafCount(node);
            const rowSpan = isLeaf ? Math.max(1, maxDepth - level) : 1;

            const typeLabel = window.I18n ? I18n.getTypeLabel(node.data_type || 'Text') : (node.data_type || 'Text');
            let tooltip = `${node.name}\n${node.absolute_path || node.name}`;
            if (isLeaf) {
                tooltip += `\n${t('modal_label_type') || 'Тип'}: ${typeLabel}`;
            } else {
                tooltip += `\n${t('matrix_colspan_label') || 'Ширина (колонок)'}: ${colSpan}`;
            }

            tierRows[level].push({
                node,
                colSpan,
                rowSpan,
                isLeaf,
                level,
                tooltip
            });

            if (!isLeaf) {
                node.children.forEach(child => traverse(child, level + 1));
            }
        };

        roots.forEach(root => traverse(root, 0));

        return {
            maxDepth,
            totalColumns,
            columnLabels,
            tierRows
        };
    },

    /**
     * Renders the complete multi-tier spreadsheet block matrix into containerEl.
     */
    renderMatrix(roots, containerEl) {
        if (!containerEl) return;
        containerEl.innerHTML = '';

        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);

        if (!roots || !Array.isArray(roots) || roots.length === 0) {
            containerEl.innerHTML = `
                <div class="matrix-empty-state">
                    <svg class="matrix-empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <rect x="3" y="3" width="18" height="18" rx="2"/>
                        <path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>
                    </svg>
                    <h3 data-i18n="matrix_empty_title">${this.escapeHtml(t('matrix_empty_title'))}</h3>
                    <p data-i18n="matrix_empty_hint">${this.escapeHtml(t('matrix_empty_hint'))}</p>
                </div>
            `;
            return;
        }

        const layout = this.buildMatrixLayout(roots);

        const coordHeadersHtml = layout.columnLabels
            .map(label => `<th class="matrix-coord-header">${this.escapeHtml(label)}</th>`)
            .join('');

        const rowsHtml = layout.tierRows
            .map((row, tierIdx) => {
                const cellsHtml = row.map(cell => {
                    const iconSvg = cell.isLeaf
                        ? `<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>`
                        : `<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"></path></svg>`;

                    const typeTagHtml = cell.isLeaf && cell.node.data_type
                        ? `<span class="matrix-cell-type-tag" data-type="${this.escapeHtml(cell.node.data_type)}">${this.escapeHtml(window.I18n ? I18n.getTypeLabel(cell.node.data_type) : cell.node.data_type)}</span>`
                        : '';

                    return `
                        <td class="matrix-cell ${cell.isLeaf ? 'matrix-cell-leaf' : 'matrix-cell-folder'} matrix-tier-${cell.level}"
                            colspan="${cell.colSpan}"
                            rowspan="${cell.rowSpan}"
                            title="${this.escapeHtml(cell.tooltip)}"
                            data-level="${cell.level}"
                            data-is-leaf="${cell.isLeaf}">
                            <div class="matrix-cell-content">
                                <span class="matrix-cell-icon">${iconSvg}</span>
                                <span class="matrix-cell-title">${this.escapeHtml(cell.node.name)}</span>
                                ${typeTagHtml}
                            </div>
                        </td>
                    `;
                }).join('');

                return `<tr class="matrix-tier-row matrix-tier-row-${tierIdx}">${cellsHtml}</tr>`;
            })
            .join('');

        containerEl.innerHTML = `
            <div class="matrix-scroll-wrapper">
                <table class="excel-matrix-table">
                    <thead>
                        <tr class="matrix-coord-row">
                            ${coordHeadersHtml}
                        </tr>
                    </thead>
                    <tbody>
                        ${rowsHtml}
                    </tbody>
                </table>
            </div>
        `;
    }
};

window.ExcelBlockRenderer = ExcelBlockRenderer;
