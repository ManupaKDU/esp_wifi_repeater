import re

with open("user/user_main.c", "r") as f:
    content = f.read()

# Fix the "int os_sprintf_flash" mistake I just made
content = content.replace("int os_sprintf_flash(response, \"\\r\\nInvalid Command\\r\\n\");",
                          "int len;\n    os_sprintf_flash(response, \"\\r\\nInvalid Command\\r\\n\");")

# And what about: "len = os_sprintf_flash(response, "Currently running rom %d\r\n", rboot_get_current_rom());"
# Oh wait, line 1618:
# `os_sprintf_flash(response, "Currently running rom %d\r\n", rboot_get_current_rom());`
# `to_console_len(response, os_strlen(response));`
# It's an error because `rboot_get_current_rom()` is an extra argument, but `os_sprintf_flash` expands to `ets_vsprintf(str, f, ##__VA_ARGS__)` which is correct, but wait, my regex replaced it as:
# `os_sprintf_flash(\2,\3);\n        to_console_len(\1, os_strlen(\2));`
# which means `os_sprintf_flash(response, "Currently running rom %d\r\n")` missing the `rboot_get_current_rom()` argument!

# Let's restore `user_main.c` completely, because that regex messed up any calls with `__VA_ARGS__`.
