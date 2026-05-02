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

## 2024-05-18 - Single-Input Gate Auto-Focus
**Learning:** For interstitial or security "gate" pages (like device lock screens) that contain only a single primary input field, users face unnecessary friction if they must manually focus the field before typing.
**Action:** Always apply `autofocus` and `required` attributes to the primary input on single-input interstitial pages to reduce friction and prevent empty submissions. Pair with visually hidden asterisks (`aria-hidden='true'`) on labels for sighted users.

## 2024-05-18 - C Preprocessor Token Limits
**Learning:** When modifying embedded HTML macros in C header files, be incredibly cautious around existing preprocessor directives. Compilers (like xtensa-gcc) will throw fatal errors if syntax (like closing parentheses or semicolons `));`) is placed on the exact same line following an `#endif` directive, because it treats them as illegal extra preprocessor tokens.
**Action:** Always ensure any closing syntax or logic continues on a new line *after* an `#endif` block when resolving macro strings in C.

## 2024-05-18 - Nested C Macros Syntax Errors
**Learning:** Found another syntax error in the same codebase caused by mismatched closing parentheses during refactoring nested macros (`acl_show(i, response));`).  
**Action:** When tracking down CI build failures in C codebases, closely inspect the line for stray tokens when parentheses are chained heavily at the end of statements.

## 2024-05-18 - Non-destructive Form Feedback
**Learning:** Overwriting `document.body.innerHTML` to provide feedback after form submission is destructive. It removes all screen reader context, breaks layout, and is an inaccessible pattern, especially in embedded web interfaces without external pages to redirect to.
**Action:** Use a pre-rendered, visually hidden `<div role='status'>` and toggle its visibility (e.g., via `style.display`) when providing feedback. Update `document.title` to robustly announce state changes without layout shifts.
## 2025-01-28 - Synchronize dynamic states for auxiliary inputs
**Learning:** When dynamically disabling a primary input field (like a password field when security is set to 'Open'), leaving auxiliary controls associated with that field (like a 'Show Password' checkbox) enabled creates an inconsistent and confusing UI state.
**Action:** Always ensure any auxiliary controls tied to a primary input are disabled synchronously alongside the primary field to maintain a consistent UI state and avoid user confusion.

## 2023-10-27 - Inline Validation for Embedded Systems
**Learning:** In constrained embedded web interfaces where backend error handling might result in a confusing generic error page or silent truncation, client-side input validation is crucial. Relying on HTML5 attributes like `maxlength`, `pattern`, and `title` provides immediate feedback to the user and prevents malformed data from ever reaching the device, improving both UX and device stability.
**Action:** Use standard HTML5 validation attributes (`maxlength`, `minlength`, `pattern`) whenever adding or modifying configuration inputs for embedded interfaces to ensure inputs conform to expected formats (e.g., IPv4 addresses, SSID lengths).

## 2025-01-28 - HTML5 minlength validation insight
**Learning:** HTML5 validation attributes like `minlength` will not be evaluated if the field is empty unless the `required` attribute is also present. This is particularly relevant when input fields (like passwords) are dynamically enabled or disabled based on other settings. Without `required`, an empty field with `minlength='8'` is considered valid and will allow submission, which can lead to silent failures or backend-generated defaults.
**Action:** When enforcing minimum length constraints on input fields, especially those that can be disabled conditionally, always pair `minlength` with the `required` attribute to ensure proper client-side validation when the field is enabled.

## 2025-01-28 - Placeholder Attributes in Embedded Devices
**Learning:** In embedded configuration pages where external help documentation is sparse or unavailable, adding `placeholder` attributes (e.g., `placeholder='Min 8 characters'`) to inputs provides valuable, inline guidance to users. Additionally, visually denoting unconditionally required fields with an asterisk (e.g., `*`) combined with `<span aria-hidden='true'>*</span>` informs sighted users about the field's requirement without cluttering screen reader announcements, which already handle the native `required` attribute.
**Action:** Use `placeholder` attributes liberally in embedded HTML configurations to offer immediate user guidance. Hide visual required indicators (like asterisks) from screen readers using `aria-hidden='true'` since the native HTML5 `required` attribute already conveys this state natively.

## 2024-06-25 - Add native dark mode support to config pages
**Learning:** Adding `<meta name="color-scheme" content="light dark">` enables native browser dark mode support automatically for unstyled native HTML elements without needing CSS changes. This is highly beneficial for the unstyled embedded web interface of ESP8266 where memory constraints limit custom CSS.
**Action:** Use the `color-scheme` meta tag early when building highly constrained native interfaces to ensure a base level of accessibility for users preferring dark mode.

## 2026-05-02 - ARIA Live Regions vs DOM Replacement in Embedded UIs
**Learning:** Destructively replacing `document.body.innerHTML` for submission feedback on embedded config pages breaks screen reader context and creates jarring visual shifts.
**Action:** Use a pre-rendered `<div role='status'>` and toggle its visibility while hiding the form (`display: none`) and updating the `<title>` to cleanly announce state changes while preserving semantic structure.
