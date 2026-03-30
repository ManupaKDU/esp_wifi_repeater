## 2026-03-13 - Optimize String Building
**Learning:** In C, repeated string concatenation using os_sprintf(&buffer[os_strlen(buffer)], ...) causes an O(N^2) performance bottleneck (Schlemiel the Painter's algorithm).
**Action:** Always maintain a len variable when appending to a buffer in a loop to keep time complexity at O(N).
## 2026-03-13 - Prevent Memory Leaks on Station Queries
**Learning:** Codebase Architecture/Performance pattern: In the ESP8266 SDK, `wifi_softap_get_station_info()` dynamically allocates memory for a linked list of connected stations. This memory *must* be manually freed using `wifi_softap_free_station_info()` after use.
**Action:** Always ensure that any loop over `station_info` retrieved via `wifi_softap_get_station_info` ends with a call to `wifi_softap_free_station_info` to prevent severe heap memory leaks and eventual application crashes.
## 2026-03-14 - Cache os_sprintf Return Value
**Learning:** Codebase performance pattern: Avoid redundant `os_strlen()` calls on buffers immediately after writing to them with `os_sprintf()`. Because `os_sprintf()` returns the number of characters written, capture and use this return value directly to prevent unnecessary O(N) string traversals.
**Action:** Always capture the return value of `os_sprintf` when the string length is needed immediately afterwards.
