/**
 * Tree Renderer Module
 * Handles DOM generation for workspace nodes and leaf path badges.
 */

const TreeRenderer = {
    renderTree(roots, containerEl) {
        containerEl.innerHTML = '';
        if (!roots || roots.length === 0) {
            document.getElementById('treeEmptyState').style.display = 'flex';
            return;
        }
        document.getElementById('treeEmptyState').style.display = 'none';

        roots.forEach(root => {
            const nodeEl = this.createNodeElement(root);
            containerEl.appendChild(nodeEl);
        });
    },

    createNodeElement(node) {
        const wrapper = document.createElement('div');
        wrapper.className = 'tree-node';
        wrapper.dataset.id = node.id;
        wrapper.dataset.isContainer = node.is_container;

        const content = document.createElement('div');
        content.className = 'tree-node-content';
        content.draggable = true;
        content.dataset.id = node.id;

        const folderIcon = `<svg class="node-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 2h9a2 2 0 012 2z"/></svg>`;
        const leafIcon = `<svg class="node-icon leaf" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6"/></svg>`;

        const iconHtml = node.is_container ? folderIcon : leafIcon;

        content.innerHTML = `
            <div class="node-left">
                <span class="drag-handle" title="Drag to reorder or nest">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 6h.01M8 12h.01M8 18h.01M16 6h.01M16 12h.01M16 18h.01"/></svg>
                </span>
                ${iconHtml}
                <span class="node-title">${this.escapeHtml(node.name)}</span>
                <span class="node-path-badge">${this.escapeHtml(node.absolute_path)}</span>
            </div>
            <div class="node-actions">
                ${node.is_container ? `<button class="action-btn add-child" title="Add Child Node" data-id="${node.id}">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
                </button>` : ''}
                <button class="action-btn delete" title="Delete Node" data-id="${node.id}">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
                </button>
            </div>
        `;

        wrapper.appendChild(content);

        // Render Children if container
        if (node.is_container && node.children && node.children.length > 0) {
            const childrenContainer = document.createElement('div');
            childrenContainer.className = 'tree-children';
            node.children.forEach(child => {
                childrenContainer.appendChild(this.createNodeElement(child));
            });
            wrapper.appendChild(childrenContainer);
        }

        return wrapper;
    },

    renderPaths(roots, pathListEl) {
        pathListEl.innerHTML = '';
        const leafPaths = [];

        function collectLeafPaths(node) {
            if (!node.is_container || !node.children || node.children.length === 0) {
                leafPaths.push(node.absolute_path);
            } else {
                node.children.forEach(collectLeafPaths);
            }
        }

        if (roots) {
            roots.forEach(collectLeafPaths);
        }

        document.getElementById('pathCountBadge').textContent = `${leafPaths.length} Paths`;

        if (leafPaths.length === 0) {
            pathListEl.innerHTML = `<div class="empty-state"><p>No leaf paths generated yet</p></div>`;
            return;
        }

        leafPaths.forEach(path => {
            const pathCard = document.createElement('div');
            pathCard.className = 'path-card';
            pathCard.textContent = path;
            pathListEl.appendChild(pathCard);
        });
    },

    escapeHtml(str) {
        return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
};
