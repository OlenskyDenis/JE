/**
 * Unique Level Hierarchy View Renderer (Features 028, 030, 033)
 * Deconstructs multi-root tree forests into horizontal stacked level rows
 * containing deduplicated unique header terms partitioned into leaf elements first
 * and branch elements second, separated by an aesthetic visual paragraph divider.
 */

const UniqueLevelRenderer = {
    escapeHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    },

    extractUniqueLevels(roots) {
        if (window.UniqueLevelExtractor) {
            return UniqueLevelExtractor.extractUniqueLevels(roots);
        }
        return [];
    },

    renderChipsList(itemsList) {
        if (!itemsList || itemsList.length === 0) return '';
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);

        return itemsList.map(item => {
            const freqBadgeHtml = item.count > 1
                ? `<span class="chip-freq-badge" title="${this.escapeHtml(t('level_unique_stat', { count: item.count }))}">×${item.count}</span>`
                : '';
            const crossMatchBadgeHtml = item.isCrossMatch
                ? `<span class="chip-cross-badge">${this.escapeHtml(t('chip_match_badge', { levels: item.matchingLevels.join(', ') }))}</span>`
                : '';

            return `
                <div class="level-header-chip ${item.isCrossMatch ? 'has-cross-match' : ''} ${item.isFolder ? 'is-branch-chip' : 'is-leaf-chip'}"
                     data-term="${this.escapeHtml(item.normalized)}"
                     data-node-id="${this.escapeHtml(item.nodeId)}"
                     data-node-name="${this.escapeHtml(item.name)}"
                     data-data-type="${this.escapeHtml(item.dataType || 'Text')}"
                     data-is-folder="${item.isFolder}"
                     data-node-ids="${this.escapeHtml(item.nodeIds.join(','))}"
                     data-count="${item.count}"
                     title="${this.escapeHtml(item.tooltip)}">
                    <span class="chip-title">${this.escapeHtml(item.name)}</span>
                    ${freqBadgeHtml}${crossMatchBadgeHtml}
                </div>
            `;
        }).join('');
    },

    renderUniqueLevels(roots, containerEl) {
        if (!containerEl) return;
        containerEl.innerHTML = '';
        const t = (k, p) => (window.I18n ? I18n.t(k, p) : k);

        if (!roots || !Array.isArray(roots) || roots.length === 0) {
            containerEl.innerHTML = `
                <div class="unique-levels-empty-state">
                    <svg class="unique-levels-empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M4 6h16M4 12h16M4 18h16"/><circle cx="8" cy="6" r="2"/><circle cx="16" cy="12" r="2"/><circle cx="10" cy="18" r="2"/>
                    </svg>
                    <h3 data-i18n="unique_levels_empty_title">${this.escapeHtml(t('unique_levels_empty_title'))}</h3>
                    <p data-i18n="unique_levels_empty_hint">${this.escapeHtml(t('unique_levels_empty_hint'))}</p>
                </div>
            `;
            return;
        }

        const levelRows = this.extractUniqueLevels(roots);
        const rowsHtml = levelRows.map(row => {
            const hasLeaves = row.leafItems && row.leafItems.length > 0;
            const hasBranches = row.branchItems && row.branchItems.length > 0;
            let groupsHtml = '';

            if (hasLeaves) {
                const leafChipsHtml = this.renderChipsList(row.leafItems);
                const leafHeaderHtml = (hasLeaves && hasBranches)
                    ? `<div class="level-subgroup-header"><span class="level-subgroup-title">${this.escapeHtml(t('level_subgroup_leaves'))}</span><span class="level-subgroup-pill level-subgroup-pill-leaf">${row.leafItems.length}</span></div>`
                    : '';
                groupsHtml += `<div class="level-subgroup level-group-leaves">${leafHeaderHtml}<div class="level-chips-container">${leafChipsHtml}</div></div>`;
            }

            if (hasLeaves && hasBranches) {
                groupsHtml += `<div class="level-group-separator" role="separator"><span class="level-group-separator-line"></span></div>`;
            }

            if (hasBranches) {
                const branchChipsHtml = this.renderChipsList(row.branchItems);
                const branchHeaderHtml = (hasLeaves && hasBranches)
                    ? `<div class="level-subgroup-header"><span class="level-subgroup-title">${this.escapeHtml(t('level_subgroup_branches'))}</span><span class="level-subgroup-pill level-subgroup-pill-branch">${row.branchItems.length}</span></div>`
                    : '';
                groupsHtml += `<div class="level-subgroup level-group-branches">${branchHeaderHtml}<div class="level-chips-container">${branchChipsHtml}</div></div>`;
            }

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
                    <div class="level-subgroups-wrapper">${groupsHtml}</div>
                </div>
            `;
        }).join('');

        containerEl.innerHTML = `<div class="unique-levels-wrapper">${rowsHtml}</div>`;
        this.bindHoverSync(containerEl);
    },

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
