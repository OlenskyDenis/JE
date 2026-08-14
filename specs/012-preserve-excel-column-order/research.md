# Research & Architectural Decisions: Preservation of Original Excel Column Sequence

**Feature**: 012-preserve-excel-column-order  
**Date**: 2026-08-14  

## Decision 1: FIFO Insertion-Order Deduplication in `HeaderService.process_headers`

- **Context**: In previous versions, `HeaderService.process_headers` executed `cleaned_headers.sort(key=lambda s: (s.lower(), s))`, which alphabetized headers. When streaming Row 1 from Excel, this altered the column sequence from left-to-right into alphabetical order.
- **Decision**:
  - Remove the `.sort(...)` call from `HeaderService.process_headers`.
  - Maintain `seen = set()` for $O(1)$ duplicate checking, appending each unique trimmed non-empty header string to `cleaned_headers` in its exact first-seen order (FIFO).
- **Rationale**: Preserves the original left-to-right domain sequence of spreadsheet columns as authored by users or database engineers.

## Decision 2: Natural Left-to-Right Hierarchy Tree Construction in `PathParserService`

- **Context**: `PathParserService.parse_header_paths` processes header path strings sequentially, creating root nodes and child subtrees via `add_root` and `add_child` (append).
- **Decision**:
  - With `HeaderService` providing headers in true left-to-right column order, `PathParserService` automatically constructs the multi-root forest and all child sub-branches in the exact first-encounter order from left to right.
  - No changes needed in `WorkspaceForest` or `PathParserService` beyond ensuring no hidden sorting calls exist.

## Decision 3: Test Suite Updates

- **Context**: `tests/unit/test_header_service.py` contained assertions specifically checking that `["b", "A", "c"]` was sorted to `["A", "b", "c"]`.
- **Decision**:
  - Refactor `tests/unit/test_header_service.py` to assert that `["Zebra", "Alpha", "Beta"]` is preserved as `["Zebra", "Alpha", "Beta"]`.
  - Add explicit unit tests verifying left-to-right column preservation across multi-level path trees and interspersed column branches.

## Decision 4: System Map Synchronization

- **Context**: Constitution Principle VI mandates updating `.specify/system_map.md`.
- **Decision**: Update `HeaderService` and `ExcelHierarchyAdapter` descriptions in `.specify/system_map.md` to reflect insertion-order preservation.
