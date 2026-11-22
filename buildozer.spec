[app]
title = CART3R Dynamic Island
package.name = cart3rdynamic
package.domain = org.cart3r
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0

android.api = 34
android.minapi = 23
android.ndk = 25b
android.permissions = INTERNET
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1