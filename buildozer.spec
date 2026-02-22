[app]
title = SciCalc Pro
package.name = scicalc
package.domain = org.indrascicalc
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Library sangat penting! Sympy butuh mpmath.
requirements = python3,kivy==2.2.1,kivymd==1.1.1,sympy,mpmath

# Izin (biasanya kalkulator tidak butuh internet, jadi aman dikosongkan untuk keamanan)
android.permissions = 

# Bootstrap
p4a.branch = master
# Arsitektur (hapus x86 jika hanya untuk HP modern biar APK kecil)
android.archs = arm64-v8a

# Layar penuh
fullscreen = 1
