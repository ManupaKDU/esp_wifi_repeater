import re
with open('user/user_main.c', 'r') as f:
    content = f.read()

# Fix syntax error in acl_show call
content = content.replace("acl_show(i, response));", "acl_show(i, response);")

with open('user/user_main.c', 'w') as f:
    f.write(content)
