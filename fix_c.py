import re

with open('user/user_main.c', 'r') as f:
    content = f.read()

content = content.replace("#endif#if HAVE_ENC28J60", "#endif\n#if HAVE_ENC28J60")
content = content.replace("#endif#if ALLOW_SCANNING", "#endif\n#if ALLOW_SCANNING")
content = content.replace("espconn_send(pespconn, (uint8_t *) send_data, sizeof(send_data) - 1);#if ACLS", "espconn_send(pespconn, (uint8_t *) send_data, sizeof(send_data) - 1);\n#if ACLS")

with open('user/user_main.c', 'w') as f:
    f.write(content)
