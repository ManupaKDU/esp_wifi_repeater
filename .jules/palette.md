## 2025-01-28 - Dynamic disable for irrelevant form fields
**Learning:** In router configuration interfaces, allowing users to enter a password when the security mode is set to "Open" is a common source of confusion. Similarly, silent backend generation of random WPA2 passwords when the user input is too short is a poor UX pattern. Client-side validation is important even in embedded devices.
**Action:** Always dynamically disable irrelevant input fields based on the state of related controls (e.g., disable password when security is "Open"). Use HTML5 validation attributes like `minlength` to enforce backend constraints on the client-side to provide immediate feedback to the user before submission.
## 2024-05-24 - HTML5 Validation inside C Macros
**Learning:** When embedding HTML within C macro strings (like in embedded firmware web servers), HTML5 regex `pattern` attributes must avoid characters that could trigger escape sequences or require complex escaping (e.g., using `[.]` instead of `\.` for literal dots). Using `inputmode='decimal'` triggers numeric keypads on mobile while keeping `type='text'` compatible with IP address patterns.
**Action:** Prefer regex character classes like `[.]` over escape sequences like `\.` to keep HTML validation strings robust and readable when embedded in C macros. Use `inputmode` to improve mobile UX for specific text formats.
## 2025-01-28 - Structural Tables Need Presentation Role
**Learning:** The embedded web interface in `user/web.h` heavily relies on HTML `<table>` elements purely for the visual layout of forms. Since external CSS is not used, this is a reasonable compromise for embedded devices, but it introduces major accessibility issues as screen readers will unnecessarily announce row and column semantics.
**Action:** Always apply `role='presentation'` to structural layout tables to prevent screen readers from announcing unnecessary tabular data, making form navigation much cleaner for visually impaired users.
## 2024-05-28 - Leveraging Native Form Validation
**Learning:** Native HTML5 validation attributes (like `required`, `minlength`) provide robust, accessible client-side feedback without the overhead of custom JavaScript. A particularly useful pattern is combining `required` with dynamic `disabled` states: a browser natively ignores validation constraints on disabled fields. This perfectly handles conditionally required fields (like a password only required when security is not "Open").
**Action:** Always prefer native HTML validation attributes over custom JavaScript validation. Use dynamic `disabled` states for conditionally required inputs to let the browser automatically manage validation logic.
## 2025-01-28 - Testing HTML embedded in C macros with static files
**Learning:** When attempting to visually verify frontend UI changes (like adding placeholders) using tools like Playwright on static HTML extracted from C format macros (e.g., `user/web.h`), any C format specifiers embedded in `value` attributes (like `value='%s'`) will render as literal strings. Because an `input` with a value will hide its `placeholder`, this prevents visual verification of the new placeholders.
**Action:** When extracting embedded HTML macros for static testing, manually clear `value` attributes that contain C format specifiers (e.g., using `sed "s/value='%s'/value=''/g" test_ui.html`) to ensure placeholders and empty states can be accurately verified.
## 2025-01-28 - Visual indicator for required fields without screen reader redundancy
**Learning:** For unconditionally required fields, visually denoting them with an asterisk informs sighted users of the requirement. However, appending an asterisk to the label directly will cause screen readers to announce it, creating redundant or confusing audio output, because the native HTML `required` attribute already correctly handles the screen reader logic for required fields.
**Action:** Wrap the required asterisk in a `<span aria-hidden='true'>*</span>` to visually denote the required field without causing redundant screen reader announcements.
## 2025-01-28 - Show Password Toggle for improved usability and security
**Learning:** For embedded device web interfaces, default password inputs to `type='password'` for security, and pair them with an adjacent 'Show Password' toggle (e.g., a checkbox with an inline `onclick` handler). This allows users to easily verify their input without exposing it by default.
**Action:** When adding or modifying password fields, ensure they are of type password and consider adding an adjacent show password toggle, especially for fields prone to typos like WiFi passwords.

## 2024-05-15 - Prevent empty lock submissions & add lock help text
**Learning:** Destructive or highly impactful actions (like locking a device interface) that require an explicit user confirmation via a checkbox can be confusing if the associated submit button remains active. Users may accidentally submit the form empty. Additionally, failing to inform the user beforehand which password will be needed to unlock creates anxiety and bad UX.
**Action:** Disable the submit button natively via an inline `disabled` attribute and dynamically enable it using `onchange="document.getElementById('lock_submit').disabled = !this.checked;"`. Add explicit `aria-describedby` helper text explaining the unlock mechanism *before* the user locks themselves out.

## 2024-05-24 - Autofocus and Required for Single-Input Pages
**Learning:** For single-input gate pages (like a lock or unlock screen), adding autofocus and required attributes significantly reduces user friction and prevents empty form submissions.
**Action:** Always add `autofocus` and `required` to the primary input field on single-input interstitial or gate pages.
