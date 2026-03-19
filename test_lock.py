import re

with open('user/web.h', 'r') as f:
    content = f.read()

lock_page = re.search(r'#define LOCK_PAGE "(.*?)"', content, re.DOTALL)
if lock_page:
    html = lock_page.group(1).replace('\\\n', '\n')
    print(html)
