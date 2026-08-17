/**
 * Unique Level Extractor (Feature 028, 030, 033)
 * Pure algorithmic module for extracting, deduplicating, and partitioning
 * multi-root hierarchy trees into stacked depth levels with leaf-first grouping.
 */

const UniqueLevelExtractor = {
    /**
     * Extracts and deduplicates unique header terms per depth level,
     * classifying each term as leaf or branch, and computing cross-level
     * term overlap across the entire forest.
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
                    isFolder: false,
                    count: 0,
                    paths: [],
                    dataTypes: new Set()
                };
                levelMaps[depth].set(norm, entry);
            }

            const nodeHasChildren = !!(node.children && Array.isArray(node.children) && node.children.length > 0);
            if (nodeHasChildren) {
                entry.isFolder = true;
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
                    isLeaf: !item.isFolder,
                    count: item.count,
                    paths: item.paths,
                    dataTypes: Array.from(item.dataTypes),
                    matchingLevels,
                    isCrossMatch,
                    tooltip
                };
            });

            // Partition items: Leaf elements first (no children), Branch elements second (with children)
            const leafItems = items.filter(it => !it.isFolder);
            const branchItems = items.filter(it => it.isFolder);

            // Sort each group alphabetically for clean scannability
            leafItems.sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: 'base' }));
            branchItems.sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: 'base' }));

            const sortedItems = [...leafItems, ...branchItems];
            const crossMatchCount = items.filter(it => it.isCrossMatch).length;
            const title = lvl === 0
                ? t('level_roots_title')
                : t('level_tier_title', { level: lvl });

            return {
                level: lvl,
                title,
                uniqueCount: items.length,
                leafCount: leafItems.length,
                branchCount: branchItems.length,
                crossMatchCount,
                leafItems,
                branchItems,
                items: sortedItems
            };
        });
    }
};

window.UniqueLevelExtractor = UniqueLevelExtractor;
