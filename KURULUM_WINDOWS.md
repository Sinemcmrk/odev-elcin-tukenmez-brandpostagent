# Windows Kurulum ve Kullanım Rehberi

Toplam süre: ilk kurulum yaklaşık 15 dakika, örnek üretimi yaklaşık 15 dakika.
Komut yazmanız gerekmez; her adım bir dosyaya çift tıklamaktır.

---

## Adım 1 — Python'u kurun (bir kez)

1. https://www.python.org/downloads/ adresine gidin ve **Python 3.12** sürümünü indirin
   (sayfada daha yeni bir sürüm öne çıkıyorsa, "All releases" listesinden 3.12'yi seçin; en sorunsuz sürüm budur).
2. Kurulum penceresinin en altındaki **“Add python.exe to PATH”** kutusunu mutlaka işaretleyin.
3. **Install Now**'a tıklayın ve kurulumu bitirin.

## Adım 2 — Proje klasörünü açın

1. `BrandPostAgent.zip` dosyasına sağ tıklayın → **Tümünü ayıkla**.
2. Hedef olarak kısa bir klasör seçin, örneğin `C:\BrandPostAgent`
   (OneDrive ile eşitlenen Masaüstü klasörleri kurulumu yavaşlatabilir).

## Adım 3 — Kurulumu çalıştırın (bir kez)

1. Klasördeki **`kurulum.bat`** dosyasına çift tıklayın.
2. Windows “Windows bilgisayarınızı korudu” uyarısı gösterirse **Ek bilgi → Yine de çalıştır**'a tıklayın.
3. Siyah pencerede paketler ve Chromium yüklenir (3–8 dakika). Sonunda **Not Defteri** ile `.env` dosyası açılır.

## Adım 4 — Ücretsiz Gemini API anahtarını alın ve yapıştırın

1. https://aistudio.google.com/apikey adresine Google hesabınızla girin.
2. **Create API key** (API anahtarı oluştur) butonuna tıklayın ve anahtarı kopyalayın.
3. Açılan `.env` dosyasında şu satırı bulun ve anahtarı yapıştırın:
   ```
   GEMINI_API_KEY=AIza...sizin_anahtariniz...
   ```
4. **Dosya → Kaydet** ile kaydedip Not Defteri'ni kapatın.

> **Ücretsiz kalmak için:** Google Cloud'da bu proje için **faturalandırmayı (billing) açmayın**.
> Agent ücretli bir servise geçmez; kota dolarsa bekler ya da durup mesaj verir.
> Anahtarınızı kimseyle paylaşmayın ve `.env` dosyasını maile eklemeyin.

## Adım 5 — (İsteğe bağlı) Testleri çalıştırın

**`test_calistir.bat`** → 35 agent testi (`35/35 test geçti`), 14 arayüz akış kontrolü (`15/15 arayüz kontrolü geçti`) ve tasarım çeşitliliği testi (`ÇEŞİTLİLİK TESTİ GEÇTİ`). Toplam 6–10 dakika.
Bu testler gerçek Gemini'yi kullanmaz, internet ve anahtar gerektirmez.

## Adım 6 — Uygulamayı başlatın ve bir post üretin

1. **`baslat.bat`** dosyasına çift tıklayın. Birkaç saniye sonra tarayıcıda `http://localhost:8501` açılır
   (açılmazsa bu adresi tarayıcıya kendiniz yazın).
2. Sol paneldeki **Bağlantıyı test et** butonuna basın → “Bağlantı başarılı. Kullanılacak model: …” görmelisiniz.
3. **Post üret** sekmesinde:
   - **Marka** ve **Platform** seçin (Instagram Feed ana platformdur; Instagram Story ikincil seçenektir).
   - **Post konusu / isteğiniz** alanını doldurun (ör. *Sınav haftasında uyku hakkında yanlış bilinenler*).
   - Tarih, sayı, kabul sonucu gibi bilgiler kullanılacaksa **Doğrulanmış bilgi** alanına yazın. Agent bilgi uydurmaz.
   - **Tasarım (kompozisyon)** kutusunu “Otomatik” bırakabilir ya da 8 kompozisyondan birini seçebilirsiniz.
   - **1 · Plan hazırla (Agent 1)** butonuna basın.
4. Agent 1 eksik bilgi görürse (ör. seminer duyurusunda tarih yoksa) **kısa sorular** sorar. Yanıtlayıp **Yanıtlarla devam et**'e basın
   ya da **Bilgi vermeden devam et** seçeneğini kullanın. Genel bilgilendirici postlarda soru sorulmaz.
5. **Plan ekranı:** niyet, seçilen seri, sayfa sayfa metinler, caption, hashtag'ler ve tasarım planı (renkler, fontlar, logo yeri) görünür.
   - Değişiklik istiyorsanız **Geri bildirim** alanına yazıp **Geri bildirimi uygula**'ya basın. Agent 1 planın yeni sürümünü hazırlar.
   - **Başka tasarım dene** bölümünde aynı konu için 2–3 farklı kompozisyon önizlemesiyle görünür. **Bu tasarımı dene** ile
     içerik o tasarıma göre yeniden yazılır. Geri bildirime “Bunu infografik yap” ya da “Carousel olarak anlat” yazmak da tasarımı değiştirir.
   - Zemini değiştirmek için **Görünümü değiştir** listesinden başka bir tema seçip **Görünümü uygula**'ya basın (renkler Brand Kit içindedir).
   - Metni kendiniz düzeltmek için **Metni elle düzenle** bölümünü kullanın.
   - Beğendiğinizde **Onayla ve görseli üret (Agent 2)** butonuna basın. **Onay vermeden görsel üretilmez.**
6. Agent 2 PNG'leri üretir. Görselleri tek tek ya da **Tümünü indir (ZIP)** ile indirebilirsiniz; ZIP'te caption ve onaylı plan da bulunur.
   Her üretim ayrıca `outputs\` klasörüne kaydedilir. Yeni bir post için **Yeni post** butonunu kullanın.
7. Kapatmak için siyah pencereyi kapatın.

## Adım 7 — Teslim için örnek postları üretin

1. **`ornekler_uret.bat`** dosyasına çift tıklayın. Her marka için 4 Feed ve 1 Story (toplam 20) sırayla işlenir.
   Tasarımı Agent 1 otomatik seçer; örnek setinde aynı kompozisyon tekrar seçilirse farklı yerleşimli alternatife geçilir.
2. Her örnekte Agent 1'in planı siyah pencerede görünür. Klavyeden seçin ve Enter'a basın:
   **O** = onayla ve görseli üret · **G** = geri bildirim ver · **A** = atla.
   Agent bir soru sorarsa yanıtı yazın ya da boş bırakıp Enter'a basın.
3. Bittiğinde `ornekler\` klasöründe her örneğin PNG'leri, `caption.txt`, `plan_onayli.json` ve `post.json` dosyaları;
   ayrıca **`ornekler\OZET.md`** ve **`ornekler\ozet.png`** oluşur. Toplam süre yaklaşık 20 dakikadır.
4. Yarıda kalırsa (ör. kota) dosyayı tekrar çalıştırın; tamamlanan örnekler atlanır.
5. Uygulamadaki **Örnek çıktılar** sekmesi bu örnekleri gösterir.

---

## Sık karşılaşılan sorunlar

| Mesaj | Çözüm |
|---|---|
| `Python bulunamadı` | Adım 1'i tekrarlayın, “Add python.exe to PATH” kutusunu işaretleyin, bilgisayarı yeniden başlatın. |
| `API anahtarı geçersiz` | `.env` dosyasındaki anahtarı kontrol edin (boşluk ya da tırnak olmamalı), kaydedip uygulamayı yeniden başlatın. |
| `Ücretsiz katmanın dakikalık sınırı` | 1 dakika bekleyip tekrar deneyin. |
| `Günlük kotası doldu` | Kota Türkiye saatiyle yaklaşık 10.00'da yenilenir. Agent otomatik olarak başka bir ücretsiz modele geçmeyi dener. |
| `Model bulunamadı (404)` | `.env` içinde `GEMINI_MODEL=auto` olduğundan emin olun. |
| `Görsel üretilemedi` | `kurulum.bat`'ı tekrar çalıştırın (Chromium eksik olabilir). |
| Tarayıcı açılmadı | Adres çubuğuna `http://localhost:8501` yazın. |
| Kurum/okul ağında bağlantı hatası | Ağ Google API'lerini engelliyor olabilir; ev ağı veya telefon internetiyle deneyin. |
