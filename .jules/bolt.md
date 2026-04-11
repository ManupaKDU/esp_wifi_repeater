## 2026-03-13 - Optimize String Building
**Learning:** In C, repeated string concatenation using os_sprintf(&buffer[os_strlen(buffer)], ...) causes an O(N^2) performance bottleneck (Schlemiel the Painter's algorithm).
**Action:** Always maintain a len variable when appending to a buffer in a loop to keep time complexity at O(N).

## 2026-03-14 - Redundant String Length Calculation
**Learning:** Calling `os_strlen` on a string immediately after `os_sprintf` is redundant, because `os_sprintf` (and `snprintf`) already returns the exact number of characters written. This redundancy forces a double-pass over the string.
**Action:** Whenever a string length is needed immediately after formatting, capture the `os_sprintf` return value instead of doing a separate `os_strlen` pass. This is especially critical in tight formatting loops.
