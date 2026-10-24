# Test ve Durum Raporu — Final Sürüm

Tarih: 22–23 Ekim 2026

## 1. Sorun analizi: Agent neden hep aynı tasarımı üretiyordu?

Gerçek Gemini testinde aynı markanın postları birbirine çok benziyordu. Kod incelendiğinde sorunun **örnek üreticiden değil,
şablon sisteminin kendisinden** kaynaklandığı görüldü:

| Bulgu | Etkisi |
|---|---|
| Agent her markada yalnızca 4–5 seri kullanabiliyordu ve bunların çoğu aynı iskeletteydi (üst etiket → büyük başlık → kutu → CTA → alt bant). E4I'nin tüm serileri “halka bandı + başlık + renkli çubuk”, Design House'unkiler “şarap zemin + altta dar başlık” düzenindeydi. | Konu değişse de kompozisyon değişmiyordu. |
| Post Kütüphanesi'ndeki 5 seri agent'a hiç eklenmemişti (Sınav Pasaportu, Sayılarla, Global Network, Six Paths, By the Numbers); görsel olarak en farklı olanlar bunlardı. | Kütüphane ile agent tutarsızdı, çeşitlilik kaybolmuştu. |
| Bir önceki sürümde eklenen görünüm temaları yalnızca rengi değiştiriyordu. | Kullanıcı aynı düzenin renk varyasyonlarını gördü. |
| Seçimde alternatif, geçmiş ve “başka tasarım” mekanizması yoktu; model geçersiz seri önerirse ilk seri kullanılıyordu. | Aynı seri art arda seçilebiliyordu. |

## 2. Yapılan değişiklikler (mevcut mimari korunarak)

- **Her markada 8 Feed kompozisyon ailesi + 1 Story.** Kütüphanede olup agent'ta olmayan 5 seri eklendi; her markaya gerçek
  Instagram postlarına ve web sitesine dayanan 2 yeni aile yazıldı:
  ABA Psikoloji *Soru Bandı* ve *Alıntı Kartı*, ABA Eğitim *Slogan* ve *Fotoğraflı Duyuru*, E4I *Process Infographic* ve
  *Innovation Spotlight*, Design House *Service Block* ve *Badge Lesson*. Her ailenin yerleşim tipi, uygun içerik türü ve fotoğraf
  kullanımı `agent/series.py › FAMILY` içinde tanımlı.
- **Akıllı seçim (`agent/design.py`):** Agent 1 aileleri açıklamalarıyla görür, son kullanılan kompozisyonları bilir ve 2 alternatif
  önerir. Kod, içerik uygunluğuna göre adayları sıralar ve son kullanılan yerleşime küçük bir ceza verir. Öncelik sırası:
  marka kimliği → içerik uygunluğu → çeşitlilik.
- **Başka tasarım dene:** Plan ekranında 2–3 farklı yerleşimli alternatif, önizlemeleriyle gösterilir. Liste ek Gemini çağrısı
  harcamaz; seçim 1 çağrıyla içeriği yeni şablona göre yeniden yazar. “Bunu infografik yap”, “carousel olarak anlat” gibi geri
  bildirimler seriyi değiştirir.
- **Fotoğraf yuvası:** 6 ailede kullanıcının yüklediği fotoğraf tasarımın parçası olur; fotoğraf yoksa marka grafikleri kullanılır.
- **Kütüphane–kod tutarlılığı:** Post Kütüphanesi PDF'leri artık agent'ın şablon kodundan üretiliyor (tek kaynak). Her marka için
  13 sayfa: 8 seri + Story sayfası, her seride tasarım referansı kutusu.
- **Örnek üretici:** Tasarımı Agent 1 otomatik seçer; örnek setinde aynı yerleşim tekrar seçilirse agent'ın önerdiği farklı
  yerleşimli alternatife geçilir.
- Korunanlar: iki aşamalı akış, SHA-256 onay kapısı, ücretsiz Gemini istemcisi, doğruluk denetimleri, Feed 1080×1350 ve Story 1080×1920.

## 3. Testler

**Önemli:** Bu ortamdan Google API'lerine erişim yok. Aşağıdaki testlerin tamamı **sahte Gemini sunucusuyla**
(`tests/mock_gemini.py`) yapıldı. Görseller gerçek Chromium ile üretildi ve ölçüldü. Sahte sunucunun metinleri kütüphane
örneklerinden türetilir; **bunlar gerçek agent çıktısı değildir.** Gerçek Gemini bağlantısı kullanıcının bilgisayarında önceki
sürümde çalıştı (bağlantı testi, plan ve PNG üretimi); bu final sürüm henüz gerçek Gemini ile çalıştırılmadı.

### 3.1 Agent testleri — `python -m tests.run_tests` → **35/35 geçti**

| # | Test |
|---|---|
| 1–6 | Doğruluk denetimleri: uydurma sayı/yüzde/tarih, kullanıcı bilgisi, karakter sınırı, HTML temizleme, hashtag ve dil |
| 7–10 | Gemini istemcisi: ücretsiz model seçimi, geçersiz anahtar, dakikalık ve günlük kota (ücretli servise geçmeden durma) |
| 11 | Tüm şablonlar örnek içerikle taşmadan çizilir: 32 Feed serisi + 4 Story, ölçüler doğru |
| 12–15 | Niyet ve soru: genel postta soru yok, etkinlikte tarih sorulur, yanıt kullanılır, başarı duyurusu bilgi ister |
| 16–17 | Uydurma engeli: “20 öğrenci” denince 221 kullanılamaz; kütüphane örneği kopyalanamaz; listede olmayan okul yazılamaz |
| 18–20 | Plan ve tasarım planı, geri bildirim (marka dışı istek uygulanmaz), elle düzenleme |
| 21–22 | Onay kapısı (onaysız / onaydan sonra değişmiş plan reddedilir), onay sonrası tüm carousel sayfaları |
| 23–24 | Dört marka · Feed 1080×1350 ve Story 1080×1920 |
| 25–28 | Marka kimliği kilidi, listeye sarılı Gemini yanıtı, görünüm temaları, telefon numarası yanlış alarmı |
| **29** | **Kütüphane–kod tutarlılığı:** PDF'deki her seri agent'ta, agent'taki her seri PDF'de; her markada 8 farklı yerleşim; tüm önizlemeler mevcut |
| **30** | **Tasarım seçimi:** alternatifler birbirinden ve seçilen tasarımdan farklı yerleşimde; son kullanılan kompozisyon geride kalır; geçmiş kaydedilir |
| **31** | **Başka tasarım:** “Bu tasarımı dene” farklı seriye ve yerleşime geçer (yeni sürüm, onay sıfırlanır); “Bunu infografik yap” → Process Infographic |
| **32** | **Fotoğraf yuvası:** fotoğraf yüklenince tasarımın parçası olur, yüklenmezse grafik yedek kullanılır |
| 33–35 | Çift kaçırma hatası (& → &amp;amp;) giderildi, platform kaydı, fotoğraf katmanı |

### 3.2 Arayüz akış testi — `python -m tests.app_smoke` → **15/15 geçti**

Streamlit bu ortama kurulamadığı için `app.py` taklit bir Streamlit modülüyle baştan sona çalıştırıldı: istek → plan (PNG yok)
→ geri bildirim → görünüm değişikliği → elle düzenleme → **Bu tasarımı dene** (farklı seri) → onay → PNG + indirme →
yeni post → marka kartıyla seçim → soru → yanıt → Story → PNG. Tarayıcıdaki görünüm test edilmedi; yalnızca başlık alanı ve marka
kartları aynı CSS ile Chromium'da çizilip kontrol edildi.

**Arayüz görünümü (son eklenen):** Agent logosu ve giriş alanı, logolu marka kartları, seçilen markanın rengine geçen vurgu rengi
(butonlar, adım çubuğu, sekmeler). Logolar markaların kendi logo dosyalarıdır (`templates/assets/ui`, `araclar/ui_gorselleri.py`).

### 3.3 Tasarım çeşitliliği testi — `python -m tests.cesitlilik_testi` → **GEÇTİ** (sahte Gemini)

Her marka için `ornekler_uret.py`'deki 4 Feed konusu, gerçek akışla (otomatik tasarım seçimi → onay → Agent 2) üretildi.
Karşılaştırma görselleri: `tests/cesitlilik_testi/<marka>.png`, ayrıntı: `sonuc.json`.

**Yerleşim farkı ölçüsü:** Görsellerin kenar haritaları (yalnızca şekil, renk değil) karşılaştırıldı. Ölçütün doğruluğu için aynı
şablonun iki renk teması da ölçüldü: **0,835** (renk farklı, düzen aynı). Farklı kompozisyonlarda bu değer **0,24–0,43** arasında kaldı.

| Marka | Post (seçilen seri · yerleşim · tema) | Sayfa | Ölçü | Taşma |
|---|---|---|---|---|
| ABA Psikoloji | Alıntı Kartı · ortalanmış alıntı · — | 1 | 1080×1350 | Yok |
| | Ebeveyn Rehberi · soru kutusu · bordo | 1 | 1080×1350 | Yok |
| | Mit vs Gerçek · carousel karşılaştırma · koyu | 4 | 1080×1350 | Yok |
| | Haftanın Rutini · adım listesi · krem | 1 | 1080×1350 | Yok |
| ABA Eğitim | “Keşke” Listesi · numaralı carousel · lacivert | 4 | 1080×1350 | Yok |
| | Sınav Programı · dev başlık · krem | 1 | 1080×1350 | Yok |
| | Fotoğraflı Duyuru · tam sayfa görsel · — | 1 | 1080×1350 | Yok |
| | Slogan · ortalanmış tipografi · lacivert | 1 | 1080×1350 | Yok |
| E4I | Process Infographic · ikonlu infografik · mor | 1 | 1080×1350 | Yok |
| | Future Careers · alan kartı · açık | 1 | 1080×1350 | Yok |
| | Playbook · carousel adım · mor | 4 | 1080×1350 | Yok |
| | Innovation Spotlight · büyük görsel · koyu | 1 | 1080×1350 | Yok |
| Design House | Portfolio Lesson · pano ders · krem | 1 | 1080×1350 | Yok |
| | Build Your Future · siyah CTA · şarap (ilk seçim Portfolio Lesson'dı; tekrar olduğu için alternatife geçildi) | 1 | 1080×1350 | Yok |
| | Destinations · şehir carousel'i · şarap | 4 | 1080×1350 | Yok |
| | Service Block · bölünmüş blok · — | 1 | 1080×1350 | Yok |

Her markanın 4 postu 4 farklı yerleşim ailesinden geldi; en yüksek yerleşim benzerliği: Psikoloji 0,39 · Eğitim 0,43 · E4I 0,24 ·
Design House 0,40. Markaya uygunluk: logo, renk paleti, font ve iletişim bandı şablonda sabit; tüm postlarda korunuyor.

## 4. Gerçek kullanımda bulunan ve düzeltilen hatalar

- Gemini yanıtı listeye sarılı geldi (`[{...}]`) → her iki biçim okunuyor.
- Kabul Duyurusu'nda “20 öğrenci” denince 221 yazıldı (örnek ve geçmiş paylaşım kopyalandı) → örnek değerler gizlendi, sayı ve
  okullar yalnızca kullanıcı bilgisinden; uydurma sayı içeren plan onaylanamaz.
- Telefon numarası “uydurma sayı” sanıldı → telefonlar denetim dışı.
- Future Careers'ta ürün adı alan adı gibi yazıldı, kapanış etiketi tekrarladı → seri kuralları ve tekrar denetimi.
- Her konu aynı düzende çıktı → bu sürümün ana konusu (bölüm 1–2).
- (Son kuru çalıştırmada bulundu) `ornekler_uret` içinde onaylanamayan plan programı durduruyordu → artık nedeni yazılıp
  G/A seçeneği sunuluyor. Soruları boş bırakılan "son tarih" konusunda, bilgi gerektiren seri yerine bilgi gerektirmeyen
  en uygun kompozisyon seçiliyor (tarih uydurulmuyor).

### 4.1 Örnek üretici kuru çalıştırması (sahte Gemini)

`ornekler_uret.py` sahte Gemini sunucusuyla baştan sona çalıştırıldı: **20/20 örnek** (4 marka × 4 Feed + 1 Story) onaylanıp
üretildi, hata yok. Bu çıktılar sahte metin içerdiği için pakete konmadı; gerçek örnekler kullanıcı tarafından `ornekler_uret.bat`
ile gerçek Gemini üzerinden üretilecek.

## 5. Test edilemeyenler (açıkça)

1. **Final sürümün gerçek Gemini ile çalışması.** İstek biçimi önceki sürümle aynı; yeni alanlar (`alternatives`, `design_reason`,
   `switch_series`) eksik gelirse kod bunları kendisi tamamlar. İlk gerçek deneme kullanıcının bilgisayarında olacak.
2. **Gerçek modelin tasarım kararları.** Çeşitlilik testi sahte bir “model” ile yapıldı. Gerçek modelin seçimleri farklı olabilir;
   alternatifler ve “Başka tasarım dene” bu yüzden her planda kullanıcıya sunulur.
3. **Gerçek Streamlit arayüzünün görünümü** ve **Windows** (önceki sürüm kullanıcının Windows bilgisayarında çalıştı).
4. **Agent örnek postları:** Pakette yok; `ornekler_uret.bat` ile gerçek Gemini üzerinden, kullanıcının onayıyla üretilir.

## 6. Bilinen sınırlamalar

- Metin kalitesi ücretsiz Flash-Lite modeline bağlıdır; geri bildirim ve “Başka tasarım dene” ile düzeltilebilir.
- Doğruluk denetimi kurala dayalıdır: sayı, tarih ve okul adı yakalanır; sayı içermeyen yanlış iddia yakalanamaz. Onay adımı bu yüzden zorunludur.
- Agent görsel üretmez (ücretli görsel API'si yok); fotoğraf ancak kullanıcı yüklerse kullanılır ve kullanım hakkı kullanıcının sorumluluğundadır.
- Her ailenin yerleşimi bilinçli olarak sabittir (seri sistemi); çeşitlilik aileler arasındadır.
- Story her marka için tek düzendir.
