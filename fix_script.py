import re

with open('user/user_main.c', 'r') as f:
    content = f.read()

new_macro = """#define os_sprintf_flash(str, fmt, ...)                                    \\
    ({                                                                     \\
        static const char flash_str[] ICACHE_RODATA_ATTR STORE_ATTR = fmt; \\
        int flen = (sizeof(flash_str) + 4) & ~3;                           \\
        char *f = (char *)os_malloc(flen);                                 \\
        os_memcpy(f, flash_str, flen);                                     \\
        int len = ets_vsprintf(str, f, ##__VA_ARGS__);                     \\
        os_free(f);                                                        \\
        len;                                                               \\
    })"""

old_macro = """#define os_sprintf_flash(str, fmt, ...)                                    \\
    do                                                                     \\
    {                                                                      \\
        static const char flash_str[] ICACHE_RODATA_ATTR STORE_ATTR = fmt; \\
        int flen = (sizeof(flash_str) + 4) & ~3;                           \\
        char *f = (char *)os_malloc(flen);                                 \\
        os_memcpy(f, flash_str, flen);                                     \\
        ets_vsprintf(str, f, ##__VA_ARGS__);                               \\
        os_free(f);                                                        \\
    } while (0)"""

content = content.replace(old_macro, new_macro)

with open('user/user_main.c', 'w') as f:
    f.write(content)
