## 2026-03-13 - Optimize String Building
**Learning:** In C, repeated string concatenation using os_sprintf(&buffer[os_strlen(buffer)], ...) causes an O(N^2) performance bottleneck (Schlemiel the Painter's algorithm).
**Action:** Always maintain a len variable when appending to a buffer in a loop to keep time complexity at O(N).
## 2026-03-13 - Prevent Memory Leaks on Station Queries
**Learning:** Codebase Architecture/Performance pattern: In the ESP8266 SDK, `wifi_softap_get_station_info()` dynamically allocates memory for a linked list of connected stations. This memory *must* be manually freed using `wifi_softap_free_station_info()` after use.
**Action:** Always ensure that any loop over `station_info` retrieved via `wifi_softap_get_station_info` ends with a call to `wifi_softap_free_station_info` to prevent severe heap memory leaks and eventual application crashes.

## 2024-03-29 - Avoid Redundant os_strlen After os_sprintf
**Learning:** In C, calling `os_strlen(buffer)` immediately after writing to `buffer` with `os_sprintf(...)` is a redundant O(N) scan.
**Action:** Always capture the integer return value of `os_sprintf` (which is the number of characters written) to determine the string length directly, avoiding the need for `os_strlen`.
