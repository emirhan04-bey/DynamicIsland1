# CART3R Dynamic Island

Python + Kivy ile hazırlanmış Android uygulama içi Dynamic Island prototipi.

## Özellikler
- Uygulama içinde sürüklenebilir Dynamic Island
- Ada genişliği ve yüksekliği ayarı
- X/Y konum ayarı
- Altı renk seçeneği
- Kontrol merkezi görünümü
- Wi-Fi, Bluetooth, ses ve ekran Android ayarlarına kısayollar

## Önemli sınır
Bu sürüm sistem genelinde diğer uygulamaların üzerinde kayan gerçek bir overlay değildir.
Bildirim dinleme, kilit ekranı entegrasyonu ve sistem genelinde Dynamic Island için ayrıca
Android native foreground service, overlay izni ve bildirim erişimi gerekir.
Android 10+ sürümlerde normal uygulamalar Wi-Fi'yi doğrudan açıp kapatamaz; bu proje
Android'in Wi-Fi ayar sayfasını açar.

## APK oluşturma
Buildozer Linux ortamında çalışır. Android telefonun üzerinde tek başına bu klasöre
dokunmak APK üretmez. Linux bilgisayar veya uygun bir Linux bulut ortamı gerekir.

1. Python 3 ve Buildozer kur:
   `pip install --user buildozer`
2. Proje klasörüne gir:
   `cd CART3R_Dynamic_Island`
3. APK oluştur:
   `buildozer android debug`
4. APK, `bin/` klasöründe oluşur.

İlk derleme Android SDK/NDK dosyalarını indireceği için uzun sürebilir.

## Çalıştırma (masaüstü test)
`pip install kivy`
`python main.py`