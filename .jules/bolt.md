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

## 2026-03-14 - Optimize MAC Formatting Overhead
**Learning:** Codebase C/ESP8266 pattern: Use the built-in `MACSTR` and `MAC2STR()` macros directly within `os_sprintf` calls instead of allocating intermediate `uint8_t` stack buffers and using custom conversion functions (like `mac_2_buff`). This reduces stack memory usage and eliminates unnecessary function-call overhead during string formatting.
**Action:** When building formatted strings in loops, inline formatting helpers that internally use `os_sprintf` (such as `mac_2_buff`) directly into the parent `os_sprintf` call.


**Learning:** Codebase performance pattern: using `mac_2_buff` to format MAC addresses into intermediate stack-allocated string buffers (`uint8_t buffer[20]`) before passing them to `os_sprintf` via `%s` adds unnecessary memory pressure and redundant formatting overhead.
**Action:** Use the built-in `MACSTR` format string macro combined with the `MAC2STR(mac_array)` argument macro to inline MAC address formatting directly into the target `os_sprintf` call. This reduces stack allocation (saving ~20 bytes per MAC address) and eliminates the need for intermediate helper function calls.

## 2024-06-28 - Avoid os_sprintf for Single Character Append
**Learning:** C/ESP8266 Performance Pattern: Using `os_sprintf` to append a single literal character (e.g., `os_sprintf(&buffer[len], ",");`) invokes unnecessary overhead from variadic arguments and format parsing inside loops.
**Action:** Replace single-character `os_sprintf` calls with direct array assignment (e.g., `buffer[len] = ',';`) to avoid formatting overhead and improve string building performance.

## 2024-06-29 - Optimize single-character string appends in loops
**Learning:** C/ESP8266 Performance Pattern: Using `os_sprintf` to append a single literal character (e.g., `os_sprintf(&buffer[len], ",");`) invokes unnecessary overhead from variadic argument handling and format string parsing, especially inside loops.
**Action:** Replace it with direct array assignment (e.g., `buffer[len] = ','; buffer[len + 1] = '\0';`) for a safe and functionally equivalent micro-optimization.

## 2024-06-30 - Replace os_sprintf with direct array assignment for single characters
**Learning:** Using `os_sprintf` to append a single literal character (e.g., `os_sprintf(&buffer[len], ",");`) invokes unnecessary overhead from variadic argument handling and format string parsing, especially inside loops.

## 2026-03-14 - Avoid os_sprintf for single character appends
**Learning:** C/ESP8266 Performance Pattern: Using `os_sprintf` to append a single literal character (e.g., `os_sprintf(&buffer[len], ",");`) invokes unnecessary overhead from variadic argument handling and format string parsing, especially inside loops.
## 2026-07-04 - Optimize Single Character Appends in C
**Learning:** Using `os_sprintf` to append a single literal character (e.g., `os_sprintf(&buffer[len], ",");`) invokes unnecessary overhead from variadic argument handling and format string parsing, especially inside loops.
**Action:** Replace it with direct array assignment and manual null-termination (e.g., `buffer[len] = ','; buffer[len + 1] = '\0';`) for a safe and functionally equivalent micro-optimization.

## 2024-05-24 - Conditionally skip redundant work in periodic timer callbacks
**Learning:** Codebase C/ESP8266 Performance Pattern: When optimizing periodic timer callbacks (like telemetry reporting), do not use early returns (`return;`) to skip redundant work, as this can silently bypass necessary state updates (like time tracking `t_old = t_new`) at the end of the callback function.
**Action:** Instead, securely wrap the expensive operations in a conditional block (e.g., `if (config.mqtt_topic_mask != 0) { ... }`) to avoid executing redundant function calls while ensuring state updates run.

## 2024-05-18 - Securely optimize periodic callbacks
**Learning:** Codebase C/ESP8266 Performance Pattern: When optimizing periodic timer callbacks (like telemetry reporting), do not use early returns (`return;`) to skip redundant work, as this can silently bypass necessary state updates (like time tracking `t_old = t_new`) at the end of the callback function.
**Action:** Securely wrap the expensive operations in a conditional block (e.g., `if (config.mqtt_topic_mask != 0) { ... }`) to avoid early returns and ensure state updates are reached.

## 2026-06-18 - Replace Software Division with Bitwise Shift on Hot Paths
**Learning:** Codebase performance pattern: ESP8266 lacks a hardware division unit, making software division (e.g., `get_long_systime() / 1000000ULL`) take significantly more CPU cycles than bitwise operations. When calculating timestamps for TTL logic inside high-frequency networking paths (like per-packet bridge forwarding), this adds measurable overhead.
**Action:** Replace division by 1,000,000 with a right bitwise shift by 20 (`>> 20`, dividing by 1,048,576) to approximate seconds. This reduces a multi-cycle division to a single-cycle shift instruction, dramatically speeding up the packet processing hot path while retaining functionally identical TTL expiration behavior.

## 2024-06-24 - Avoid 64-bit Software Division on Hot Paths
**Learning:** C/ESP8266 Performance Pattern: The ESP8266 lacks a hardware division unit, making 64-bit software division (e.g., / 1000000ULL) computationally expensive.
**Action:** On hot paths where slight precision loss is acceptable (like internal TTL timeouts in packet processing), replace division by 1,000,000 with a right bitwise shift by 20 (>> 20, dividing by 1,048,576) to optimize performance, and add a comment explaining the ~4.8% acceptable drift.

## 2026-07-05 - Block Skip Telemetry Processing
**Learning:** In periodic telemetry callbacks, checking `mqtt_enabled` and `interval` is not enough. If the user disabled specific MQTT topics via `mqtt_topic_mask == 0`, the code executes dozens of formatting calculations and function calls (like `mqtt_publish_int`), only for each inner function to exit due to mask checks.
**Action:** Add an early block check for `config.mqtt_topic_mask != 0` around the telemetry processing. This O(1) check skips all subsequent O(N) formatting and redundant mask checks, saving significant CPU cycles when telemetry is disabled, while safely preserving timer callback state updates outside the block.

## 2026-03-14 - Skip Expensive Work Early
**Learning:** Codebase C/ESP8266 Performance Pattern: When optimizing periodic timer callbacks (like telemetry reporting), do not use early returns (`return;`) to skip redundant work, as this can silently bypass necessary state updates (like time tracking `t_old = t_new`) at the end of the callback function. Instead, securely wrap the expensive operations in a conditional block (e.g., `if (config.mqtt_topic_mask != 0) { ... }`).
**Action:** When optimizing callback functions, wrap the expensive operations in conditionals rather than using early returns to ensure crucial state cleanup operations at the end of the function remain intact.

## 2026-07-17 - Wrap Redundant Execution in Early Exit
**Learning:** Codebase C/ESP8266 Performance Pattern: When optimizing periodic timer callbacks (like telemetry reporting), do not use early returns (`return;`) to skip redundant work, as this can silently bypass necessary state updates (like time tracking `t_old = t_new`) at the end of the callback function. Instead, securely wrap the expensive operations in a conditional block (e.g., `if (config.mqtt_topic_mask != 0) { ... }`).
**Action:** When a telemetry mask is 0, wrap all subsequent redundant formatting, memory allocation, string generation, and MQTT publish calls in a conditional block, while ensuring time tracking variables are properly updated.

## 2026-03-14 - Skip Redundant MQTT Work When Topics Are Disabled
**Learning:** Codebase C/ESP8266 Performance Pattern: When optimizing periodic timer callbacks (like telemetry reporting), do not use early returns (`return;`) to skip redundant work, as this can silently bypass necessary state updates (like time tracking `t_old = t_new`) at the end of the callback function.
**Action:** Instead of early returns, securely wrap the expensive operations (function calls, math, hardware queries) in a conditional block (e.g., `if (config.mqtt_topic_mask != 0) { ... }`).

## 2026-07-24 - Prevent Expensive Argument Evaluations
**Learning:** Function arguments in C are evaluated before the function is called. When calling telemetry functions (like `mqtt_publish_int`) that internally check if a topic is enabled, any expensive operations passed as arguments (like software divisions e.g., `Bytes_in / 1024`) will always be executed, even if the topic is disabled.
**Action:** When a block of code conditionally executes based on a bitmask (e.g., `config.mqtt_topic_mask != 0`), wrap the function calls at the caller level to prevent evaluating expensive arguments when the entire feature is disabled, while ensuring necessary state updates at the end of the callback are not skipped.

## 2026-07-25 - Avoid Unnecessary Argument Evaluation in C
**Learning:** Function arguments in C evaluate before the function call. When calling functions that might internally exit early (like mqtt_publish_int checking topic masks), expensive arguments (like software divisions Bytes_in / 1024 on ESP8266, which lacks hardware division) will still evaluate.
**Action:** Wrap such calls in a caller-level conditional block to skip unnecessary computation, instead of relying on the function's internal early return. However, ensure that necessary state updates following the block are not mistakenly bypassed.

## 2026-07-27 - Prevent Expensive Argument Evaluations
**Learning:** Function arguments in C are evaluated before the function is called. When calling telemetry functions (like `mqtt_publish_int`) that internally check if a topic is enabled, any expensive operations passed as arguments (like software divisions e.g., `Bytes_in / 1024`) will always be executed, even if the topic is disabled.
**Action:** When a block of code conditionally executes based on a bitmask (e.g., `config.mqtt_topic_mask != 0`), wrap the function calls at the caller level to prevent evaluating expensive arguments when the individual topic is disabled in the mask, and use bitwise shift (e.g., `>> 10`) instead of division by 1024 to save cycles.

## 2026-07-29 - Replace Software Division by Powers of 2 with Bitwise Shifts
**Learning:** C/ESP8266 Performance Pattern: Unlike approximating `/ 1000000` with `>> 20` (which introduces inaccuracy and should be avoided), explicitly replacing divisions by exact powers of 2 (e.g., `/ 1024`) with bitwise right shifts (e.g., `>> 10`) on unsigned integers maintains perfect correctness while saving software division CPU cycles on chips lacking hardware division.
**Action:** On hot paths (like packet processing and telemetry updates) and elsewhere, safely replace divisions by 1024 with right bitwise shifts by 10 (`>> 10`) to speed up execution time with zero loss in precision.
## 2026-08-02 - Cache Expensive String Comparisons on Network Hot Paths
**Learning:** Codebase C/ESP8266 Performance Pattern: Checking configuration state (like `config.ssid == WIFI_SSID`) using string comparison functions (`os_strcmp`) directly inside per-packet network callbacks (like `bridge_input_ap`) forces expensive byte-by-byte memory iterations and function call overhead for every single frame.
**Action:** When a configuration string is known to only change across reboots (or explicitly triggered re-initializations), cache the result of the string comparison into a static boolean during initialization (`bridge_init`) to reduce per-packet overhead to a single boolean check.

## 2026-08-04 - Cache Expensive String Comparisons on Hot Paths
**Learning:** C/ESP8266 Performance Pattern: Avoid evaluating expensive string comparisons (e.g., `os_strcmp`) directly inside per-packet network hot paths (like `bridge_input_ap`).
**Action:** Cache the result into a static boolean during initialization to minimize per-packet processing overhead.

## 2024-05-12 - Cache Expensive String Comparisons on Hot Paths
**Learning:** C/ESP8266 Performance Pattern: Evaluating expensive string comparisons (e.g., `os_strcmp`) directly inside per-packet network hot paths (like `bridge_input_ap`) adds significant processing overhead to every single packet.
**Action:** Cache the result of static string comparisons into a static boolean during initialization to minimize per-packet processing overhead.

## 2026-07-30 - Cache Expensive String Comparisons on Network Hot Paths
**Learning:** C/ESP8266 Performance Pattern: Avoid evaluating expensive string comparisons (e.g., `os_strcmp`) directly inside per-packet network hot paths (like `bridge_input_ap`).
**Action:** Instead, cache the result into a static boolean during initialization (e.g., `bridge_init`) to minimize per-packet processing overhead.

## 2026-08-06 - Cache SSID String Comparison in Hot Paths
**Learning:** C/ESP8266 Performance Pattern: Avoid evaluating expensive string comparisons (e.g., `os_strcmp(config.ssid, WIFI_SSID)`) directly inside per-packet network hot paths (like `bridge_input_ap`).
**Action:** Cache the result into a static boolean during initialization (`bridge_init`) to minimize per-packet processing overhead.

## 2024-08-12 - Defer Memory Allocation on Network Hot Paths
**Learning:** C/ESP8266 Performance Pattern: On high-frequency network hot paths (like `bridge_input_ap` and `bridge_input_sta`), defer dynamic memory allocation (`pbuf_alloc`) and buffer copying (`pbuf_copy`) until after evaluating early return conditions (e.g., local MAC address matches).
**Action:** Move early return checks before heap operations to avoid expensive allocation overhead for dropped or non-bridged packets.
