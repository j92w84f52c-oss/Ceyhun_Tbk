# Instagram Reels Editörü — Brief

Ham (editlenmemiş) bir konuşma videosunu CapCut, Edits veya Premiere kullanmadan, kodla (ffmpeg, Python, HTML/CSS ile grafik) editleyip yayına hazır 9:16 bir Reels'e çevir.

Ortam kurulumu: `bash tools/setup.sh`

## HESAP BİLGİLERİ
- Hesap adı: [@kullaniciadin]
- Konu: [ör. çalışan anneler, bebek bakımı, çocukla günlük hayat]
- Hedef kitle: [ör. 25-40 yaş çalışan anneler]
- Dil: Türkçe (altyazılarda Türkçe karakterler ş, ğ, ı, İ, ç, ö, ü doğru görünmeli)

## ÇALIŞMA SIRASI (adımları atlama)
1. ANALİZ: Videoyu dinle ve kelime kelime, zaman damgalı bir transkript çıkar. Videonun süresini, çözünürlüğünü ve ses seviyesini raporla.
2. TEMİZLİK PLANI: Şunları tespit edip liste halinde göster:
   - Uzun sessizlikler (0,4 saniyeden uzun)
   - Hatalı başlangıçlar, tekrar edilen cümleler (aynı cümleyi iki kez söylediysem son ve en iyi halini tut)
   - "ııı", "eee", "şey", "yani" gibi dolgu sesleri
   - Kameraya hazırlandığım baş ve son kısımları
3. STORYBOARD: Editlemeye başlamadan önce her sahne için bir kare ve altına: zaman aralığı, söylenen cümle, ekrana eklenecek yazı/grafik. "onay" denmeden render alma.
4. KESİM: Onaydan sonra fazlalıkları kes. Kesimler arasında ses patlaması olmasın (her kesimde 30-50 ms ses yumuşatma).
5. ALTYAZI: Konuşmayla senkron, tek seferde en fazla 2-4 kelimelik altyazı. Cümledeki en önemli kelime vurgu renginde.
6. GRAFİKLER: Anlatılanı görselleştir (stil rehberine göre).
7. SES: -14 LUFS'a normalize et. Arka plan uğultusunu hafifçe azalt, sesi bozma.
8. RENDER ve KONTROL: 1080x1920, 30 fps, H.264, AAC. Render sonrası her 2 saniyede bir kare alıp kontrol et; yazı taşması, yüze binen grafik veya senkron kayması varsa düzelt, sonra gönder.

## KURALLAR (her videoda geçerli)
1. Yüze hiçbir şey binmesin. Yazı ve grafikler yüz alanının dışında dursun.
2. Instagram arayüzünün altı boş kalsın: alttaki %20'lik alana ve sağ kenardaki butonlara hiçbir şey koyma.
3. Kafa asla kesilmesin. Zoom/kırpmada baş kadrajdan çıkmasın.
4. Vurgu rengi hep sarı (#F2C14E).
5. Konuşmayı hızlandırma. 1x hız; tempo sadece kesimlerle.
6. Efektleri kodla yap ve az kullan; sadece anlatımı güçlendiren yerlere.
7. Ses -14 LUFS.
8. Rakamları doğrula. Ekrandaki sayı söylenenle aynı olsun.
9. Önce kareleri göster. Storyboard onayı olmadan render alma.
10. Her yeri doldurma. Aynı anda en fazla 1 grafik ve 1 altyazı.
11. Nefes anları bırak: cümleler arasında 0,15-0,25 sn doğal nefes kalsın.
12. Kaynakları yaz: bilgi/istatistik/araştırmanın kaynağını küçük yazıyla köşeye ekle.

## STİL REHBERİ
- Renkler: koyu yeşil #1F3D2B, krem #F5F1E6, vurgu sarısı #F2C14E, yazı için siyah/beyaz.
- Fontlar:
  - Başlık/büyük yazılar: ince, zarif serif (Playfair Display veya Instrument Serif); vurgulanan kelime italik ve sarı.
  - Altyazı: koyu yeşil, köşeleri yuvarlatılmış kutu içinde krem serif yazı.
  - Liste, not ve kart grafikleri: JetBrains Mono, krem kart üstünde.
- Açılış (ilk 1-2 sn): ana iddia üst kısımda büyük, büyük harfli serif yazıyla (ör. "BEN EDİTLEMEDİM").
- "Peki nasıl?" geçişi: merak cümlesinden sonra 1 sn tam ekran koyu yeşil kart; üstte ince çerçeve, ortada "peki" düz, "nasıl?" italik sarı.
- Görselleştirme örnekleri:
  - Uygulama/ürün sayılıyorsa küçük logo/ikon kartları.
  - "Bunu kullanmadım" anında yazının üstü çizilsin veya kırmızı çarpı.
  - Doğru/yanlış anlatılıyorsa sarı daire veya kırmızı çarpı.
  - Liste anlatılıyorsa kart üzerinde maddeler söylendikçe tek tek belirsin.
  - Deneme–yanılma: üst üste binen "v1, v2, v3..." kartları ve sonunda yeşil "SİSTEM ✓" etiketi.
  - Süreç: kutu → ok → kutu akış şeması (ör. "ham video → Claude → Reels").
  - Kendini tanıtma anında alt-orta bölgede isim kartı ve altında hap şeklinde konu etiketleri.
- Animasyonlar: yumuşak ve kısa (0,2-0,4 sn); hafif kayma/belirme. Zıplama, dönme, abartı yok.
- Logo/filigran: [@kullaniciadin] Instagram ikonuyla, küçük ve yarı saydam, yüze binmeyen köşede.

## KAPANIŞ
- Son 5-8 saniyede yorum kutusu görünümlü kartta yorum çağrısı: "Yorumlara [ANAHTAR KELİME] yaz".
- En sonda küçük "SONRAKİ VİDEO: [konu]" kartı.

## TESLİM
- Final videoyu gönder.
- 2 farklı caption önerisi ve 5-8 hashtag.
- Kapak için videodan en iyi 3 kare önerisi.

## VİDEO NEREDE?
- Repoya yüklenir (Add file → Upload files, 25 MB'a kadar) ya da büyükse GitHub Releases'a (tag `v1`, 2 GB'a kadar) eklenir.
- Bu ortam yalnızca GitHub'a erişebiliyor; Drive/Dropbox/WeTransfer linkleri açılmaz.
- Transkript için faster-whisper modeli huggingface.co'dan iner; ortamın ağ ayarında bu alan izinli olmalı.
