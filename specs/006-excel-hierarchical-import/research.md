# Research & Architectural Decisions: Automatic Hierarchical Excel Header Import

**Feature**: 006-excel-hierarchical-import  
**Date**: 2026-08-14  

## Decision 1: Dedicated Path-to-Hierarchy Parser (`PathParserService`)

- **Context**: Row 1 header strings from an imported Excel sheet represent backslash-delimited hierarchical paths (e.g., `Root\Folder\Leaf`). We need to parse these strings into GoF Composite structures (`CompositeNode` and `LeafNode`) organized in a `WorkspaceForest`.
- **Decision**: Create a dedicated `PathParserService` in `src/hierarchy_lib/services/path_parser.py`.
- **Rationale**:
  - Adheres to Single Responsibility Principle (SRP): Decouples string path parsing from Excel file I/O (`ExcelHierarchyAdapter`) and tree manipulation (`WorkspaceForest`).
  - Highly testable with pure unit tests without requiring file fixtures.
  - Reusable across any source of hierarchical path strings.

## Decision 2: Tree Construction & Common Prefix Merging

- **Algorithm**:
  - Input: List of header strings (ordered or unordered).
  - Clean & tokenize each string: Split by `\` and strip whitespace, discarding empty segments.
  - Multi-segment paths ($k \ge 2$):
    - Root ($S_0$): Search existing `forest.root_nodes` for matching name. Create `CompositeNode` if absent.
    - Intermediates ($S_1 \dots S_{k-2}$): Search children of current container for `CompositeNode` with matching name. Create and append if absent, then step into container.
    - Leaf ($S_{k-1}$): Search children of current container for existing node with matching name. Create `LeafNode` if absent and append.
  - Single-segment paths ($k = 1$):
    - Search existing `forest.root_nodes` for matching name. Create `CompositeNode(S_0)` if absent.
- **Alternatives Considered**:
  - Creating all intermediate nodes as leaves and converting on the fly: Rejected because tree structure hierarchy requires containers to hold children.

## Decision 3: Eel Bridge Response Enrichment

- **Context**: When the frontend imports a file or switches sheets, it currently receives headers for the sidebar.
- **Decision**: Update `import_excel_file` and `switch_active_sheet` to automatically rebuild the `forest` and return `"roots": forest.to_dict()["roots"]` in the RPC response payload.
- **Rationale**:
  - Single round-trip RPC: avoids an extra `get_workspace_tree()` call from the frontend.
  - Atomic workspace state synchronization between Python backend and HTML5 frontend.
