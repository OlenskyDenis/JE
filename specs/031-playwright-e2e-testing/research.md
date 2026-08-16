# Research & Technical Analysis: Playwright E2E Integration

**Feature Branch**: `031-playwright-e2e-testing`  
**Created**: 2026-08-16  
**Status**: Ready  

---

## 1. Playwright for Python with Eel Desktop Apps

### Challenges & Solutions:

1. **Eel Web Server Lifecycle**:
   - Eel uses Bottle and Gevent/Wsgiref to serve static assets from `src/web/` and bridge Python functions with `@eel.expose`.
   - **Solution**: Start Eel with `eel.init('src/web')` and `eel.start('index.html', mode=False, port=PORT, block=True)` in a daemon background thread in `conftest.py`.

2. **Drag and Drop Simulation in Headless Chromium**:
   - Standard HTML5 Drag and Drop events (`dragstart`, `dragenter`, `dragover`, `drop`, `dragend`) require synthetic dispatch or Playwright `page.mouse` trajectory coordinates.
   - **Solution**: Use Playwright's `locator.drag_to(target_locator)` or mouse coordinate moves with step interpolation.

3. **Dialog Confirmation Handling**:
   - Deletion of nodes calls `confirm(t("confirm_delete"))`.
   - **Solution**: Use Playwright's `page.on("dialog", lambda dialog: dialog.accept())` to simulate user confirmation deterministically.
