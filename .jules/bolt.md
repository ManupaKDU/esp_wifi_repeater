## 2026-03-13 - Optimize String Building
**Learning:** In C, repeated string concatenation using os_sprintf(&buffer[os_strlen(buffer)], ...) causes an O(N^2) performance bottleneck (Schlemiel the Painter's algorithm).
**Action:** Always maintain a len variable when appending to a buffer in a loop to keep time complexity at O(N).

## 2026-03-14 - Cache Redundant SDK API Calls
**Learning:** SDK functions like `wifi_softap_get_station_num()` that retrieve hardware or network state have non-zero execution cost and can return changing values, which causes a slight race condition when evaluated multiple times in the same format string block.
**Action:** Cache the results of redundant hardware or API calls in local variables rather than invoking them multiple times within a single formatting statement or block to avoid unnecessary overhead.
