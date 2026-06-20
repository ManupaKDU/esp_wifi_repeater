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
## 2024-05-24 - Array Bounds vs String Length on Hot Paths
**Learning:** Checking equality between a dynamic buffer length and the length of a configured static array via `os_strlen` is an O(N) operation that creates unnecessary CPU overhead on extremely frequent paths, like MQTT topic matching callbacks.   
**Action:** When validating if an un-terminated string buffer matches a null-terminated configuration array, replace `len == os_strlen(config_str)` with an O(1) bounds and null-terminator check: `len < sizeof(config_str) && config_str[len] == '\0'`. 

## 2026-03-14 - Cache Redundant SDK API Calls
**Learning:** SDK functions like `wifi_softap_get_station_num()` that retrieve hardware or network state have non-zero execution cost and can return changing values, which causes a slight race condition when evaluated multiple times in the same format string block.
**Action:** Cache the results of redundant hardware or API calls in local variables rather than invoking them multiple times within a single formatting statement or block to avoid unnecessary overhead.
## 2026-03-14 - Optimize MAC address string formatting
**Learning:** Codebase C/ESP8266 pattern: Use the built-in `MACSTR` and `MAC2STR()` macros directly within `os_sprintf` calls instead of allocating intermediate `uint8_t` stack buffers and using custom conversion functions (like `mac_2_buff`). This reduces stack memory usage and eliminates unnecessary function-call overhead during string formatting.
**Action:** When printing or formatting MAC addresses, always prefer `MACSTR` with `MAC2STR(mac)` inside `os_sprintf` over writing custom wrapper functions or allocating temporary local arrays.

## 2026-03-14 - Wrap Switch Case Declarations in Blocks
**Learning:** Codebase C Syntax pitfall: In C, a variable declaration cannot immediately follow a `case` label (e.g., `case EVENT_X: int len = ...;`). This results in a strict syntax error because a label must precede a statement, and a declaration is not considered a statement.
**Action:** Always wrap the `case` block in curly braces `{ ... }` when introducing new variable declarations directly inside switch statements.

## 2024-06-13 - Avoid redundant os_strlen in MQTT publish
**Learning:** Codebase performance pattern: In `user_main.c`, strings passed to `mqtt_publish_str` are often pre-formatted using `os_sprintf` right before the call. Since `os_sprintf` returns the string length, calculating `os_strlen(str)` again inside `mqtt_publish_str` is redundant O(N) work.
**Action:** Use the new `mqtt_publish_str_len` variant which directly accepts the pre-calculated string length to save cycles.


## 2024-05-24 - Avoid Redundant string length calculation for MQTT Publish
**Learning:** Codebase performance pattern: When formatting variables (like integers) into a buffer using `os_sprintf` specifically to publish them via MQTT, passing the resulting buffer to `mqtt_publish_str` implicitly invokes a redundant `os_strlen(buf)` calculation.
**Action:** Created `mqtt_publish_str_len` to explicitly accept a string length. Refactored `mqtt_publish_int` to capture the return value of `os_sprintf(buf, ...)` and pass it directly to `mqtt_publish_str_len`, avoiding an O(N) string traversal just to find the length of the string we just wrote.

## 2026-03-14 - Avoid Optimizing Cold Paths
**Learning:** Avoid micro-optimizations (e.g., caching string lengths or replacing formatting) on 'cold' paths, such as immediately before a `system_restart()`, as this violates the optimization guidelines by adding complexity without measurable runtime benefits.
**Action:** Do not apply any performance optimizations to code blocks that execute during firmware updates, reboots, or startup sequences unless there is a proven bottleneck.

## 2026-03-14 - Inline Formatting Helpers in Loops
**Learning:** Codebase performance pattern: When building formatted strings in loops (like topology JSONs), inline formatting helpers that internally use `os_sprintf` (such as `mac_2_buff`) directly into the parent `os_sprintf` call.
**Action:** Replace intermediate buffer formatting with direct format specifiers (e.g., replacing `mac_2_buff` with `%02x:%02x:%02x:%02x:%02x:%02x`) to eliminate redundant `os_sprintf` function calls and intermediate buffer allocations inside the loop.

## 2024-05-19 - Cache redundant os_strlen in MQTT telemetry callbacks
**Learning:** Codebase performance pattern: In frequent telemetry callbacks (like publishing uptime, memory, or packet stats via MQTT), passing a buffer formatted via `os_sprintf` to a string-based publish function (e.g., `mqtt_publish_str`) triggers a redundant `os_strlen(str)` O(N) evaluation inside `MQTT_Publish`.
**Action:** Created `mqtt_publish_str_len` to directly accept a length argument. Update helper functions like `mqtt_publish_int` to capture the return value of `os_sprintf` (which returns the length) and pass it directly to `mqtt_publish_str_len`, eliminating the redundant `os_strlen` overhead.


## $(date +%Y-%m-%d) - Avoiding hardcoded string lengths for micro-optimizations
**Learning:** Do not attempt to micro-optimize string literal lengths by hardcoding integer values (e.g., `17`) or using manual calculations like `sizeof("...") - 1` in place of `os_strlen`. This creates fragile code and severe maintainability hazards, especially since compilers often optimize literal lengths automatically. Furthermore, avoid micro-optimizations on absolute cold paths (e.g., just before a `system_restart()`) as they violate the core performance directives by introducing complexity without measurable runtime benefits.
**Action:** When seeking string calculation optimizations, focus on caching dynamically calculated lengths that are already returned by upstream formatting functions (like `os_sprintf`) on hot paths, rather than trying to optimize literal lengths or cold paths.

## 2024-05-18 - Inline Formatting Helpers
**Learning:** Codebase performance pattern: When building formatted strings in loops, inline formatting helpers that internally use `os_sprintf` (such as `mac_2_buff`) directly into the parent `os_sprintf` call.
**Action:** By doing this, it prevents allocating intermediate string buffers and eliminates redundant function overhead.

## 2026-06-17 - Avoid Custom String Converters for Standard Types
**Learning:** Codebase performance pattern: Writing custom formatting wrappers like `mac_2_buff(buf, mac)` adds unnecessary function-call overhead and wastes stack memory because you must allocate intermediate string buffers (like `uint8_t mac_buf[20];`) just to hold the converted string before immediately printing it.
**Action:** Use the SDK's built-in `MACSTR` format string macro and `MAC2STR()` argument macro directly within `os_sprintf` or `os_printf` calls to format MAC addresses inline, reducing stack usage and eliminating redundant wrapper function overhead.
