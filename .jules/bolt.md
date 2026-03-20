## 2026-03-13 - Optimize String Building
**Learning:** In C, repeated string concatenation using os_sprintf(&buffer[os_strlen(buffer)], ...) causes an O(N^2) performance bottleneck (Schlemiel the Painter's algorithm).
**Action:** Always maintain a len variable when appending to a buffer in a loop to keep time complexity at O(N).
## 2026-03-13 - Avoid Redundant Function Calls
**Learning:** Calling system APIs like `wifi_softap_get_station_num()` multiple times in a single `os_sprintf` call introduces unnecessary overhead.
**Action:** Always cache the result of API/hardware calls in a local variable if the value is needed multiple times within the same block or statement.
