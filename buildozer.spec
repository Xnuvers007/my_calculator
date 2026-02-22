[app]

# (1) Judul Aplikasi
title = SciCalc Pro
package.name = scicalc
package.domain = org.indrascicalc

# (2) INI YANG HILANG TADI: Folder tempat main.py berada
source.dir = .

# (3) Ekstensi file yang akan dimasukkan ke APK
source.include_exts = py,png,jpg,kv,atlas

# (4) Versi aplikasi
version = 1.0.0

# (5) Requirements (SANGAT PENTING untuk aplikasi Anda)
# Kita memasukkan sympy dan mpmath agar kalkulator berfungsi
requirements = python3,kivy==2.2.1,kivymd==1.1.1,sympy,mpmath,sdl2_ttf==2.20.0

# (6) Orientasi Layar
orientation = portrait

# (7) Izin Android (Kalkulator biasanya tidak butuh internet)
android.permissions = 

# (8) Layar Penuh
fullscreen = 1

# (9) Bagian Android
[buildozer]
log_level = 2
warn_on_root = 1

# --- Konfigurasi Khusus Android ---
# Arsitektur (arm64-v8a untuk HP modern)
android.archs = arm64-v8a

# API Level (Target Android 13/14)
android.api = 33
android.minapi = 21
