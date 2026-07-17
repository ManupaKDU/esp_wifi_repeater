import re

with open('user/user_main.c', 'r') as f:
    content = f.read()

search = """    if (mqtt_enabled && config.mqtt_interval != 0 && (t_diff > config.mqtt_interval))
    {
        mqtt_publish_int(MQTT_TOPIC_UPTIME, "Uptime", "%d", (uint32_t)(t_new / 1000000));
        mqtt_publish_int(MQTT_TOPIC_VDD, "Vdd", "%d", Vdd);
        mqtt_publish_int(MQTT_TOPIC_BYTES, "Bin", "%d", (uint32_t)(Bytes_in / 1024));
        mqtt_publish_int(MQTT_TOPIC_BYTES, "Bout", "%d", (uint32_t)(Bytes_out / 1024));
        mqtt_publish_int(MQTT_TOPIC_PACKETS, "Ppsin", "%d", (Packets_in - Packets_in_last) / t_diff);
        mqtt_publish_int(MQTT_TOPIC_PACKETS, "Ppsout", "%d", (Packets_out - Packets_out_last) / t_diff);

        // ⚡ Bolt: Cache redundant API call for station count to avoid multiple hardware state queries
        uint8_t current_station_num = config.ap_on ? wifi_softap_get_station_num() : 0;

        mqtt_publish_int(MQTT_TOPIC_NOSTATIONS, "NoStations", "%d", current_station_num);
        mqtt_publish_int(MQTT_TOPIC_BPS, "Bpsin", "%d", (uint32_t)(Bytes_in - Bytes_in_last) / t_diff);
        mqtt_publish_int(MQTT_TOPIC_BPS, "Bpsout", "%d", (uint32_t)(Bytes_out - Bytes_out_last) / t_diff);
#if DAILY_LIMIT
        mqtt_publish_int(MQTT_TOPIC_BPD, "Bpd", "%d", (uint32_t)(Bytes_per_day / 1024));
#endif
#ifdef USER_GPIO_OUT
        mqtt_publish_int(MQTT_TOPIC_GPIOOUT, "GpioOut", "%d", (uint32_t)config.gpio_out_status);
#endif

        if (config.mqtt_topic_mask & MQTT_TOPIC_TOPOLOGY)
        {
            uint8_t *buffer = (uint8_t *)os_malloc(1024);

            if (buffer != NULL)
            {
                ip_addr_t my_ap_ip = config.network_addr;
                my_ap_ip.addr |= 0x01000000;
                uint8_t mac_buf[6];
                wifi_get_macaddr(STATION_IF, mac_buf);

                /* ⚡ Bolt: Cache redundant os_strlen calculation by capturing os_sprintf return value */
                int len = os_sprintf(buffer, "{\\"nodeinfo\\":{\\"id\\":\\"%s\\",\\"ap_mac\\":\\"" MACSTR "\\",\\"sta_mac\\":\\"" MACSTR "\\",\\"uplink_bssid\\":\\"" MACSTR "\\",\\"ap_ip\\":\\"" IPSTR "\\",\\"sta_ip\\":\\"" IPSTR "\\",\\"rssi\\":\\"%d\\",\\"mesh_level\\":\\"%u\\",\\"no_stas\\":\\"%d\\"},\\"stas\\":[",
                           config.sta_hostname, MAC2STR(config.AP_MAC_address), MAC2STR(mac_buf), MAC2STR(uplink_bssid),
                           IP2STR(&my_ap_ip), IP2STR(&my_ip),
                           wifi_station_get_rssi(),
                           config.automesh_mode == AUTOMESH_OPERATIONAL ? config.AP_MAC_address[2] : 0,
                           current_station_num);

                // Bolt: Optimize string building. Instead of recalculating the string length
                // on each iteration (O(N^2) "Schlemiel the Painter's algorithm"), we maintain
                // a 'len' variable to incrementally track the end of the buffer (O(N)).
                struct station_info *station = wifi_softap_get_station_info();
                bool do_colon = false;
                while (station)
                {
                    if (do_colon) {
                        os_sprintf(&buffer[len], ",");
                        len += 1;
                    }
                    do_colon = true;
                    len += os_sprintf(&buffer[len], "{\\"mac\\":\\"" MACSTR "\\",\\"ip\\":\\"" IPSTR "\\"}", MAC2STR(station->bssid), IP2STR(&station->ip));
                    station = STAILQ_NEXT(station, next);
                }
                wifi_softap_free_station_info();
                len += os_sprintf(&buffer[len], "]}");

                mqtt_publish_str_len(MQTT_TOPIC_TOPOLOGY, "Topology", buffer, len);
                os_free(buffer);
            }
        }

        t_old = t_new;"""


replace = """    if (mqtt_enabled && config.mqtt_interval != 0 && (t_diff > config.mqtt_interval))
    {
        /* ⚡ Bolt: Prevent redundant formatting overhead when telemetry is disabled entirely */
        if (config.mqtt_topic_mask != 0)
        {
            mqtt_publish_int(MQTT_TOPIC_UPTIME, "Uptime", "%d", (uint32_t)(t_new / 1000000));
            mqtt_publish_int(MQTT_TOPIC_VDD, "Vdd", "%d", Vdd);
            mqtt_publish_int(MQTT_TOPIC_BYTES, "Bin", "%d", (uint32_t)(Bytes_in / 1024));
            mqtt_publish_int(MQTT_TOPIC_BYTES, "Bout", "%d", (uint32_t)(Bytes_out / 1024));
            mqtt_publish_int(MQTT_TOPIC_PACKETS, "Ppsin", "%d", (Packets_in - Packets_in_last) / t_diff);
            mqtt_publish_int(MQTT_TOPIC_PACKETS, "Ppsout", "%d", (Packets_out - Packets_out_last) / t_diff);

            // ⚡ Bolt: Cache redundant API call for station count to avoid multiple hardware state queries
            uint8_t current_station_num = config.ap_on ? wifi_softap_get_station_num() : 0;

            mqtt_publish_int(MQTT_TOPIC_NOSTATIONS, "NoStations", "%d", current_station_num);
            mqtt_publish_int(MQTT_TOPIC_BPS, "Bpsin", "%d", (uint32_t)(Bytes_in - Bytes_in_last) / t_diff);
            mqtt_publish_int(MQTT_TOPIC_BPS, "Bpsout", "%d", (uint32_t)(Bytes_out - Bytes_out_last) / t_diff);
#if DAILY_LIMIT
            mqtt_publish_int(MQTT_TOPIC_BPD, "Bpd", "%d", (uint32_t)(Bytes_per_day / 1024));
#endif
#ifdef USER_GPIO_OUT
            mqtt_publish_int(MQTT_TOPIC_GPIOOUT, "GpioOut", "%d", (uint32_t)config.gpio_out_status);
#endif

            if (config.mqtt_topic_mask & MQTT_TOPIC_TOPOLOGY)
            {
                uint8_t *buffer = (uint8_t *)os_malloc(1024);

                if (buffer != NULL)
                {
                    ip_addr_t my_ap_ip = config.network_addr;
                    my_ap_ip.addr |= 0x01000000;
                    uint8_t mac_buf[6];
                    wifi_get_macaddr(STATION_IF, mac_buf);

                    /* ⚡ Bolt: Cache redundant os_strlen calculation by capturing os_sprintf return value */
                    int len = os_sprintf(buffer, "{\\"nodeinfo\\":{\\"id\\":\\"%s\\",\\"ap_mac\\":\\"" MACSTR "\\",\\"sta_mac\\":\\"" MACSTR "\\",\\"uplink_bssid\\":\\"" MACSTR "\\",\\"ap_ip\\":\\"" IPSTR "\\",\\"sta_ip\\":\\"" IPSTR "\\",\\"rssi\\":\\"%d\\",\\"mesh_level\\":\\"%u\\",\\"no_stas\\":\\"%d\\"},\\"stas\\":[",
                               config.sta_hostname, MAC2STR(config.AP_MAC_address), MAC2STR(mac_buf), MAC2STR(uplink_bssid),
                               IP2STR(&my_ap_ip), IP2STR(&my_ip),
                               wifi_station_get_rssi(),
                               config.automesh_mode == AUTOMESH_OPERATIONAL ? config.AP_MAC_address[2] : 0,
                               current_station_num);

                    // Bolt: Optimize string building. Instead of recalculating the string length
                    // on each iteration (O(N^2) "Schlemiel the Painter's algorithm"), we maintain
                    // a 'len' variable to incrementally track the end of the buffer (O(N)).
                    struct station_info *station = wifi_softap_get_station_info();
                    bool do_colon = false;
                    while (station)
                    {
                        if (do_colon) {
                            os_sprintf(&buffer[len], ",");
                            len += 1;
                        }
                        do_colon = true;
                        len += os_sprintf(&buffer[len], "{\\"mac\\":\\"" MACSTR "\\",\\"ip\\":\\"" IPSTR "\\"}", MAC2STR(station->bssid), IP2STR(&station->ip));
                        station = STAILQ_NEXT(station, next);
                    }
                    wifi_softap_free_station_info();
                    len += os_sprintf(&buffer[len], "]}");

                    mqtt_publish_str_len(MQTT_TOPIC_TOPOLOGY, "Topology", buffer, len);
                    os_free(buffer);
                }
            }
        }

        t_old = t_new;"""

if search in content:
    content = content.replace(search, replace)
    with open('user/user_main.c', 'w') as f:
        f.write(content)
    print("Replaced successfully in user_main.c")
else:
    print("Search string not found in user_main.c")
