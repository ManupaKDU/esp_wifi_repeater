## 2026-03-13 - Optimize String Building
**Learning:** In C, repeated string concatenation using os_sprintf(&buffer[os_strlen(buffer)], ...) causes an O(N^2) performance bottleneck (Schlemiel the Painter's algorithm).
**Action:** Always maintain a len variable when appending to a buffer in a loop to keep time complexity at O(N).
## 2024-05-18 - Optimizing String Copying Overhead
**Learning:** Many commands use `os_sprintf` or `os_sprintf_flash` followed immediately by `to_console(response)`. Since `to_console` internally calls `os_strlen(response)` to find the length to copy to the ringbuffer, this represents a redundant O(N) calculation because `os_sprintf` already returns the length of the formatted string.
**Action:** Created `to_console_len(char *str, uint16_t len)` to explicitly accept the length. By wrapping the call like `to_console_len(response, os_sprintf(response, ...))`, we eliminate the redundant `os_strlen` overhead. Always utilize the return value of formatting functions when passing to functions that need a string length.
## 2026-03-13 - Prevent Memory Leaks on Station Queries
**Learning:** Codebase Architecture/Performance pattern: In the ESP8266 SDK, `wifi_softap_get_station_info()` dynamically allocates memory for a linked list of connected stations. This memory *must* be manually freed using `wifi_softap_free_station_info()` after use.
**Action:** Always ensure that any loop over `station_info` retrieved via `wifi_softap_get_station_info` ends with a call to `wifi_softap_free_station_info` to prevent severe heap memory leaks and eventual application crashes.
## 2026-03-14 - Cache os_sprintf Return Value
**Learning:** Codebase performance pattern: Avoid redundant `os_strlen()` calls on buffers immediately after writing to them with `os_sprintf()`. Because `os_sprintf()` returns the number of characters written, capture and use this return value directly to prevent unnecessary O(N) string traversals.
**Action:** Always capture the return value of `os_sprintf` when the string length is needed immediately afterwards.
## 2024-04-03 - Compile-time String Literal Length Evaluation
**Learning:** Codebase performance pattern: Calling `os_strlen()` on string literals (e.g., `os_strlen("online")`) introduces an unnecessary O(N) runtime evaluation overhead. Because the ESP8266 `os_strlen` is often an external library function rather than an intrinsic mapped by the compiler, it can't always be optimized out by the compiler like the standard `strlen` can.
**Action:** Replace `os_strlen("literal")` with `(sizeof("literal") - 1)` to guarantee that string length evaluation is completely resolved at compile-time, saving CPU cycles and instruction memory. Note: Do not apply this to fixed-size array buffers where the runtime string length may differ from the maximum array size.
## 2024-05-18 - Avoid Micro-Optimizing I/O Bound Paths
**Learning:** In the context of console command handlers or network output, calculating `os_strlen()` on an 11-byte string literal takes a fraction of a microsecond. The latency of the underlying serial UART or network I/O completely dominates this time. Attempting to optimize such `strlen` calls with parallel arrays of pre-calculated lengths introduces complexity and degrades maintainability without any measurable performance benefit.
**Action:** Do not apply micro-optimizations (like parallel string length arrays or compile-time `sizeof` macro replacements) to non-critical, I/O-bound paths where the impact cannot be measured. Only apply these patterns in true algorithmic hot paths or large data processing loops.
## 2024-05-18 - C Macro Variable Shadowing
**Learning:** When defining multi-statement C macros using statement expressions `({ ... })` that declare local variables, those variable names must be unique (e.g., `__os_sprintf_flash_len`). Using a common name like `len` will shadow any user-provided variables of the same name passed in `__VA_ARGS__`, leading to uninitialized reads or garbage outputs.
**Action:** Always prefix local variables inside multi-statement macros with unique identifiers (like `__macro_name_var`) to prevent accidental variable shadowing.
## 2024-05-18 - C Preprocessor Syntax Pitfall
**Learning:** In C, appending trailing tokens (like parentheses `);`) on the exact same line as an `#endif` macro directive (e.g. `#endif);`) causes a strict compiler failure: "extra tokens at end of #endif directive".
**Action:** When wrapping preprocessor blocks inside function calls, always put trailing closing syntax (like `));`) on a separate line immediately following the `#endif` directive.
