[app]

# (1) Identitas Aplikasi
title = SciCalc Pro
package.name = scicalc
package.domain = org.indrascicalc

# (2) Sumber File
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# (3) Versi
version = 1.0.0

# (4) Requirements (PENTING: pillow sering dibutuhkan oleh KivyMD)
requirements = python3,kivy==2.2.1,kivymd==1.1.1,sdl2_ttf==2.20.0,pillow

# (5) Tampilan
orientation = portrait
fullscreen = 1

# (6) Izin (Kosongkan jika offline, tapi INTERNET kadang butuh untuk debug)
android.permissions = INTERNET

# --- PENGATURAN ANDROID (WAJIB DI BAWAH [app]) ---

# Arsitektur (arm64-v8a untuk HP modern)
android.archs = arm64-v8a

# API Level (Kita kunci ke 34 agar stabil)
android.api = 34
android.minapi = 21

# --- FIX UNTUK ERROR LISENSI ---
# Kita memaksa Buildozer menerima lisensi otomatis
android.accept_sdk_license = True

# Kita memaksa menggunakan Build Tools versi stabil (bukan RC)
android.build_tools_version = 34.0.0

# (Opsional) Mengunci NDK agar konsisten
android.ndk = 25b

# --- BAGIAN BUILDOZER TOOL ---
[buildozer]
log_level = 2
warn_on_root = 1
