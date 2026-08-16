/**
 * Unique Level Hierarchy View Renderer (Feature 028)
 * Deconstructs multi-root tree forests into horizontal stacked level rows
 * containing deduplicated unique header terms, with cross-level duplicate detection
 * and synchronized interactive hover highlights.
 */

const UniqueLevelRenderer = {
    escapeHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    },

    /**
     * Extracts and deduplicates unique header terms per depth level,
     * computing cross-level term overlap across the entire forest.
     */
    extractUniqueLevels(roots) {
        if (!roots || !Array.isArray(roots) || roots.length === 0) {
            return [];
        }

        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);
        const levelMaps = [];
        const termLevelsMap = new Map();

        const traverse = (node, depth) => {
            if (!node) return;
            const norm = (node.name || '').trim().toLowerCase();

            while (levelMaps.length <= depth) {
                levelMaps.push(new Map());
            }

            let entry = levelMaps[depth].get(norm);
            if (!entry) {
                entry = {
                    nodeId: node.id,
                    nodeIds: [],
                    name: node.name,
                    normalized: norm,
                    dataType: node.data_type || 'Text',
                    isFolder: !!(node.children && node.children.length > 0),
                    count: 0,
                    paths: [],
                    dataTypes: new Set()
                };
                levelMaps[depth].set(norm, entry);
            }

            entry.nodeIds.push(node.id);
            entry.count += 1;
            if (node.absolute_path) {
                entry.paths.push(node.absolute_path);
            } else {
                entry.paths.push(node.name);
            }

            if (node.data_type) {
                entry.dataTypes.add(node.data_type);
            }

            if (!termLevelsMap.has(norm)) {
                termLevelsMap.set(norm, new Set());
            }
            termLevelsMap.get(norm).add(depth);

            if (node.children && Array.isArray(node.children)) {
                node.children.forEach(child => traverse(child, depth + 1));
            }
        };

        roots.forEach(root => traverse(root, 0));

        return levelMaps.map((map, lvl) => {
            const items = Array.from(map.values()).map(item => {
                const matchingLevels = Array.from(termLevelsMap.get(item.normalized) || []).sort((a, b) => a - b);
                const isCrossMatch = matchingLevels.length > 1;

                const levelsStr = matchingLevels.join(', ');
                let tooltip = `${item.name}\n• ${t('level_unique_stat', { count: item.count })}`;
                if (isCrossMatch) {
                    tooltip += `\n• ${t('chip_match_badge', { levels: levelsStr })}`;
                }

                if (item.dataTypes.size > 0) {
                    const typesStr = Array.from(item.dataTypes)
                        .map(dt => (window.I18n ? I18n.getTypeLabel(dt) : dt))
                        .join(', ');
                    tooltip += `\n• ${t('modal_label_type') || 'Тип'}: ${typesStr}`;
                }

                const displayPaths = item.paths.slice(0, 8).map(p => `• ${p}`).join('\n');
                const morePaths = item.paths.length > 8 ? `\n... +${item.paths.length - 8}` : '';
                tooltip += `\n\nШляхи (${item.paths.length}):\n${displayPaths}${morePaths}`;
                tooltip += `\n\n${t('tooltip_dblclick_edit')}`;

                return {
                    nodeId: item.nodeId,
                    nodeIds: item.nodeIds,
                    name: item.name,
                    normalized: item.normalized,
                    dataType: item.dataType,
                    isFolder: item.isFolder,
                    count: item.count,
                    paths: item.paths,
                    dataTypes: Array.from(item.dataTypes),
                    matchingLevels,
                    isCrossMatch,
                    tooltip
                };
            });

            // Sort alphabetically for clean scannability
            items.sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: 'base' }));

            const crossMatchCount = items.filter(it => it.isCrossMatch).length;
            const title = lvl === 0
                ? t('level_roots_title')
                : t('level_tier_title', { level: lvl });

            return {
                level: lvl,
                title,
                uniqueCount: items.length,
                crossMatchCount,
                items
            };
        });
    },

    /**
     * Renders the complete level-by-level unique headers view into containerEl.
     */
    renderUniqueLevels(roots, containerEl) {
        if (!containerEl) return;
        containerEl.innerHTML = '';

        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);

        if (!roots || !Array.isArray(roots) || roots.length === 0) {
            containerEl.innerHTML = `
                <div class="unique-levels-empty-state">
                    <svg class="unique-levels-empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M4 6h16M4 12h16M4 18h16"/>
                        <circle cx="8" cy="6" r="2"/>
                        <circle cx="16" cy="12" r="2"/>
                        <circle cx="10" cy="18" r="2"/>
                    </svg>
                    <h3 data-i18n="unique_levels_empty_title">${this.escapeHtml(t('unique_levels_empty_title'))}</h3>
                    <p data-i18n="unique_levels_empty_hint">${this.escapeHtml(t('unique_levels_empty_hint'))}</p>
                </div>
            `;
            return;
        }

        const levelRows = this.extractUniqueLevels(roots);

        const rowsHtml = levelRows.map(row => {
            const chipsHtml = row.items.map(item => {
                const freqBadgeHtml = item.count > 1
                    ? `<span class="chip-freq-badge" title="${this.escapeHtml(t('level_unique_stat', { count: item.count }))}">×${item.count}</span>`
                    : '';

                const crossMatchBadgeHtml = item.isCrossMatch
                    ? `<span class="chip-cross-badge">${this.escapeHtml(t('chip_match_badge', { levels: item.matchingLevels.join(', ') }))}</span>`
                    : '';

                return `
                    <div class="level-header-chip ${item.isCrossMatch ? 'has-cross-match' : ''}"
                         data-term="${this.escapeHtml(item.normalized)}"
                         data-node-id="${this.escapeHtml(item.nodeId)}"
                         data-node-name="${this.escapeHtml(item.name)}"
                         data-data-type="${this.escapeHtml(item.dataType || 'Text')}"
                         data-is-folder="${item.isFolder}"
                         data-node-ids="${this.escapeHtml(item.nodeIds.join(','))}"
                         data-count="${item.count}"
                         title="${this.escapeHtml(item.tooltip)}">
                        <span class="chip-title">${this.escapeHtml(item.name)}</span>
                        ${freqBadgeHtml}
                        ${crossMatchBadgeHtml}
                    </div>
                `;
            }).join('');

            const matchStatHtml = row.crossMatchCount > 0
                ? `<span class="level-badge-match">${this.escapeHtml(t('level_match_stat', { count: row.crossMatchCount }))}</span>`
                : '';

            return `
                <div class="level-row-container level-tier-${row.level}">
                    <div class="level-row-header">
                        <div class="level-row-title-group">
                            <span class="level-tier-pill">Tier ${row.level}</span>
                            <h3 class="level-row-title">${this.escapeHtml(row.title)}</h3>
                            <span class="level-badge-count">${this.escapeHtml(t('level_unique_stat', { count: row.uniqueCount }))}</span>
                            ${matchStatHtml}
                        </div>
                    </div>
                    <div class="level-chips-container">
                        ${chipsHtml}
                    </div>
                </div>
            `;
        }).join('');

        containerEl.innerHTML = `
            <div class="unique-levels-wrapper">
                ${rowsHtml}
            </div>
        `;

        this.bindHoverSync(containerEl);
    },

    /**
     * Binds synchronized hover highlighting across matching terms on different levels.
     */
    bindHoverSync(containerEl) {
        if (!containerEl || containerEl._hasHoverSyncBound) return;
        containerEl._hasHoverSyncBound = true;

        containerEl.addEventListener('mouseover', (e) => {
            const chip = e.target.closest('.level-header-chip[data-term]');
            if (!chip) return;
            const term = chip.getAttribute('data-term');
            if (!term) return;

            const allMatchingChips = containerEl.querySelectorAll(`.level-header-chip[data-term="${CSS.escape(term)}"]`);
            if (allMatchingChips.length > 1) {
                allMatchingChips.forEach(c => c.classList.add('highlight-match-sync'));
            }
        });

        containerEl.addEventListener('mouseout', (e) => {
            const chip = e.target.closest('.level-header-chip[data-term]');
            if (!chip) return;
            const allActive = containerEl.querySelectorAll('.highlight-match-sync');
            allActive.forEach(c => c.classList.remove('highlight-match-sync'));
        });
    }
};

window.UniqueLevelRenderer = UniqueLevelRenderer;
