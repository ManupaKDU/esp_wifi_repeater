## 2024-10-24 - Web Component Fallback Context
**Learning:** Disabled fallback buttons (like `slot="unsupported"` in `esp-web-install-button`) lack immediate context for why they are disabled, leading to user confusion.
**Action:** Explicitly add a descriptive `title` attribute to these buttons to provide an immediate tooltip explaining the missing browser API (e.g., WebUSB) and offering alternatives.
