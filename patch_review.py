import re
from datetime import datetime

with open('user/user_main.c', 'r') as f:
    content = f.read()

search = """        if (config.mqtt_topic_mask != 0)
        {
            mqtt_publish_int(MQTT_TOPIC_UPTIME, "Uptime", "%d", (uint32_t)(t_new / 1000000));"""

replace = """        /* ⚡ Bolt: Prevent redundant formatting overhead when telemetry is disabled entirely */
        if (config.mqtt_topic_mask != 0)
        {
            mqtt_publish_int(MQTT_TOPIC_UPTIME, "Uptime", "%d", (uint32_t)(t_new / 1000000));"""

if search in content:
    content = content.replace(search, replace)
    with open('user/user_main.c', 'w') as f:
        f.write(content)
    print("Replaced successfully in user_main.c")
else:
    print("Search string not found in user_main.c")

with open('.jules/bolt.md', 'r') as f:
    md_content = f.read()

date_str = datetime.now().strftime("%Y-%m-%d")
md_search = "## $(date +%Y-%m-%d) - Wrap Redundant Execution in Early Exit"
md_replace = f"## {date_str} - Wrap Redundant Execution in Early Exit"

if md_search in md_content:
    md_content = md_content.replace(md_search, md_replace)
    with open('.jules/bolt.md', 'w') as f:
        f.write(md_content)
    print("Replaced successfully in bolt.md")
else:
    print("Search string not found in bolt.md")
