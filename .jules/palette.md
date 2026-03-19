## 2024-05-24 - [Embedded HTML Accessibility]
**Learning:** Found that embedded HTML interfaces (like ESP8266 C macros) often lack basic accessibility (like `<label>` tags) and have malformed document structures (missing `<title>`, `<meta>` in body, missing table tags like `<tr>`). These are common blindspots in IoT devices.
**Action:** Always verify basic HTML structure and accessibility attributes (especially form labels) when editing embedded raw HTML strings.
## 2026-03-15 - [Destructive Action Confirmation]
**Learning:** Embedded IoT web interfaces often lack basic UX safety rails like confirmation dialogs for destructive actions (e.g. device reboots, locking).
**Action:** Add inline JS `confirm()` dialogs to buttons executing destructive actions to prevent accidental clicks. Especially important on mobile where fat-fingering is common.
## 2026-03-22 - [Mobile Input UX for Exact Strings]
**Learning:** For embedded web interfaces configuring exact string values like SSIDs, passwords, and IP addresses, mobile OS text modifications (auto-capitalization, auto-correction, spell-checking) can cause frustrating and subtle connection failures.
**Action:** Always apply `autocorrect='off'`, `autocapitalize='none'`, and `spellcheck='false'` attributes to text input fields for these exact values to prevent unwanted mobile OS text modifications.
## 2024-05-20 - Adding Core HTML Accessibility Attributes to Embedded Macros
**Learning:** Even in extremely constrained embedded interfaces that generate web pages via static C string macros, basic HTML accessibility features like `lang='en'` on the `<html>` tag and `aria-describedby` to link inputs to their helper text (e.g., minimum password lengths) are critical. They incur virtually zero overhead in the C binary size but dramatically improve screen reader experience.
**Action:** When working on embedded web interfaces (like ESP8266/ESP32 web configs), always prioritize standard HTML attributes (`lang`, `aria-describedby`) and ensure semantic tags are properly closed to build an accessible foundation.
