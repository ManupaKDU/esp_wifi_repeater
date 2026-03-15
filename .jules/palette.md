## 2024-05-24 - [Embedded HTML Accessibility]
**Learning:** Found that embedded HTML interfaces (like ESP8266 C macros) often lack basic accessibility (like `<label>` tags) and have malformed document structures (missing `<title>`, `<meta>` in body, missing table tags like `<tr>`). These are common blindspots in IoT devices.
**Action:** Always verify basic HTML structure and accessibility attributes (especially form labels) when editing embedded raw HTML strings.
## 2026-03-15 - [Destructive Action Confirmation]
**Learning:** Embedded IoT web interfaces often lack basic UX safety rails like confirmation dialogs for destructive actions (e.g. device reboots, locking).
**Action:** Add inline JS `confirm()` dialogs to buttons executing destructive actions to prevent accidental clicks. Especially important on mobile where fat-fingering is common.
