# Tasks: Unified Drag-and-Drop Interaction Handler

- [ ] T001 [Backend] Update `src/hierarchy_lib/services/forest.py` to support `add_node_at_zone` positioning for `BEFORE_SIBLING`, `AFTER_SIBLING`, and `NEST_CHILD` zones.
- [ ] T002 [Backend] Update `src/app/eel_bridge.py` RPC method `add_node` to accept `target_id` and `zone` parameters.
- [ ] T003 [Frontend] Refactor `src/web/js/drag_drop.js` to replace split state variables with unified `activeDragPayload`, unified 3-zone hit testing, and unified drop processing.
- [ ] T004 [Frontend] Update `src/web/js/app.js` to handle unified drop callback and pass `targetId` and `zone` to `eel.add_node`.
- [ ] T005 [Testing] Add unit and integration tests in Python (`tests/unit/test_forest.py`, `tests/integration/test_eel_bridge.py`) for zone-based node addition.
- [ ] T006 [Verification] Run full pytest suite to verify all backend and bridge tests pass cleanly.
