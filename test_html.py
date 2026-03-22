import re

with open('user/web.h', 'r') as f:
    content = f.read()

def clean_html(html_str):
    # Just remove the string continuation characters and backslashes that were escaping quotes
    cleaned = html_str.replace('\\\n', '')
    cleaned = cleaned.replace('\\"', '"')

    # Strip everything before <html
    idx = cleaned.find("<html")
    if idx != -1:
        cleaned = cleaned[idx:]
    return cleaned

config_page = re.search(r'#define CONFIG_PAGE "(.*?)"\n\n', content, re.DOTALL)
if config_page:
    html = clean_html(config_page.group(1))
    # Do not replace %s unconditionally to avoid breaking logic.
    html = html.replace("value='%s'", "value='test'")
    html = html.replace("value='open'%s", "value='open' selected")
    html = html.replace("value='wpa2'%s", "value='wpa2'")
    html = html.replace('%d', '0')
    with open('config_page.html', 'w') as out:
        out.write(html)

lock_page = re.search(r'#define LOCK_PAGE "(.*?)"\n', content, re.DOTALL)
if lock_page:
    html = clean_html(lock_page.group(1))
    html = html.replace('%s', 'test')
    html = html.replace('%d', '0')
    with open('lock_page.html', 'w') as out:
        out.write(html)
