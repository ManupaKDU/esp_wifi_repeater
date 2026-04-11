## 2026-03-13 - Optimize String Building
**Learning:** In C, repeated string concatenation using os_sprintf(&buffer[os_strlen(buffer)], ...) causes an O(N^2) performance bottleneck (Schlemiel the Painter's algorithm).
**Action:** Always maintain a len variable when appending to a buffer in a loop to keep time complexity at O(N).
## 2024-05-18 - Optimizing String Copying Overhead
**Learning:** Many commands use `os_sprintf` or `os_sprintf_flash` followed immediately by `to_console(response)`. Since `to_console` internally calls `os_strlen(response)` to find the length to copy to the ringbuffer, this represents a redundant O(N) calculation because `os_sprintf` already returns the length of the formatted string.
**Action:** Created `to_console_len(char *str, uint16_t len)` to explicitly accept the length. By wrapping the call like `to_console_len(response, os_sprintf(response, ...))`, we eliminate the redundant `os_strlen` overhead. Always utilize the return value of formatting functions when passing to functions that need a string length.
