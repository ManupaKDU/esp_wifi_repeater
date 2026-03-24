#define CONFIG_PAGE "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n\
<html lang='en'>\
<head>\
<meta name='viewport' content='width=device-width, initial-scale=1'>\
<title>ESP WiFi NAT Router Config</title>\
</head>\
<body>\
<h1>ESP WiFi NAT Router Config</h1>\
<div id='config'>\
<script>\
if (window.location.search.substr(1) != '')\
{\
document.getElementById('config').display = 'none';\
document.body.innerHTML ='<h1>ESP WiFi NAT Router Config</h1>The new settings have been sent to the device...';\
setTimeout(\"location.href = '/'\",10000);\
}\
</script>\
<h2>STA Settings</h2>\
<form action='' method='GET'>\
<table role='presentation'>\
<tr>\
<td><label for='sta_ssid'>SSID:</label></td>\
<td><input id='sta_ssid' type='text' name='ssid' value='%s' maxlength='32' autocorrect='off' autocapitalize='none' spellcheck='false'/></td>\
</tr>\
<tr>\
<td><label for='sta_password'>Password:</label></td>\
<td><input id='sta_password' type='password' name='password' value='%s' maxlength='63' autocorrect='off' autocapitalize='none' spellcheck='false'/></td>\
</tr>\
<tr>\
<td><label for='sta_am'>Automesh:</label></td>\
<td><input id='sta_am' type='checkbox' name='am' value='mesh' %s></td>\
</tr>\
<tr>\
<td></td>\
<td><input type='submit' value='Connect'/></td>\
</tr>\
\
</table>\
</form>\
\
<h2>AP Settings</h2>\
<form action='' method='GET'>\
<table role='presentation'>\
<tr>\
<td><label for='ap_ssid'>SSID:</label></td>\
<td><input id='ap_ssid' type='text' name='ap_ssid' value='%s' maxlength='32' autocorrect='off' autocapitalize='none' spellcheck='false'/></td>\
</tr>\
<tr>\
<td><label for='ap_password'>Password:</label></td>\
<td><input id='ap_password' type='text' name='ap_password' value='%s' minlength='8' maxlength='63' aria-describedby='ap_pwd_help' autocorrect='off' autocapitalize='none' spellcheck='false'/></td>\
</tr>\
<tr>\
<td><label for='ap_open'>Security:</label></td>\
<td>\
 <select id='ap_open' name='ap_open' onchange=\"document.getElementById('ap_password').disabled = (this.value === 'open');\">\
 <option value='open'%s>Open</option>\
 <option value='wpa2'%s>WPA2</option>\
</select>\
</td>\
</tr>\
<tr>\
<td><label for='ap_network'>Subnet:</label></td>\
<td><input id='ap_network' type='text' name='network' value='%d.%d.%d.%d' pattern='^([0-9]{1,3}[.]){3}[0-9]{1,3}$' title='Valid IP Address (e.g., 192.168.4.1)' inputmode='decimal' autocorrect='off' autocapitalize='none' spellcheck='false'/></td>\
</tr>\
<tr>\
<td></td>\
<td><input type='submit' value='Set' /></td>\
</tr>\
</table>\
<small id='ap_pwd_help'>\
<i>Password: </i>8-63 chars<br />\
</small>\
<script>document.getElementById('ap_password').disabled = (document.getElementById('ap_open').value === 'open');</script>\
</form>\
\
<h2>Lock Config</h2>\
<form action='' method='GET'>\
<table role='presentation'>\
<tr>\
<td><label for='lock_device'>Lock Device:</label></td>\
<td><input id='lock_device' type='checkbox' name='lock' value='l'></td>\
</tr>\
<tr>\
<td></td>\
<td><input type='submit' name='dolock' value='Lock'/></td>\
</tr>\
</table>\
</form>\
\
<h2>Device Management</h2>\
<form action='' method='GET'>\
<table role='presentation'>\
<tr>\
<td>Reset Device:</td>\
<td><input type='submit' name='reset' value='Restart' onclick='return confirm(\"Are you sure you want to restart the device?\");'/></td>\
</tr>\
</table>\
</form>\
</div>\
</body>\
</html>\
"

#define LOCK_PAGE "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n\
<html lang='en'>\
<head>\
<meta name='viewport' content='width=device-width, initial-scale=1'>\
<title>ESP WiFi NAT Router Config</title>\
</head>\
<body>\
<h1>ESP WiFi NAT Router Config</h1>\
<div id='config'>\
<script>\
if (window.location.search.substr(1) != '')\
{\
document.getElementById('config').display = 'none';\
document.body.innerHTML ='<h1>ESP WiFi NAT Router Config</h1>Unlock request has been sent to the device...';\
setTimeout(\"location.href = '/'\",1000);\
}\
</script>\
<h2>Config Locked</h2>\
<form autocomplete='off' action='' method='GET'>\
<table role='presentation'>\
<tr>\
<td><label for='unlock_password'>Password:</label></td>\
<td><input id='unlock_password' type='password' name='unlock_password' maxlength='63' aria-describedby='unlock_help' autocorrect='off' autocapitalize='none' spellcheck='false'/></td>\
</tr>\
<tr>\
<td></td>\
<td><input type='submit' value='Unlock'/></td>\
</tr>\
\
</table>\
<small id='unlock_help'>\
<i>Default:</i> STA password to unlock<br />\
</small>\
</form>\
</div>\
</body>\
</html>\
"
