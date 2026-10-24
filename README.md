# Brand Post Agent

ABA Psikoloji, ABA Eğitim, Education for Innovation ve Design House Global için, Brand Kit ve Post Kütüphanesi kurallarına uygun
Instagram postları (görsel + caption + hashtag) üreten iki aşamalı yapay zekâ agent'ı:
**Agent 1 planlar ve tasarımı seçer → kullanıcı onaylar → Agent 2 görseli üretir.**

- **Model:** Google Gemini, ücretsiz katman (Flash-Lite / Flash ailesi, otomatik seçim). Ücretli servise geçmez.
- **Arayüz:** Streamlit
- **Tasarım motoru:** Post Kütüphanesi'nin HTML/CSS şablonları, Playwright (Chromium) ile PNG

Kurulum: **[KURULUM_WINDOWS.md](KURULUM_WINDOWS.md)** · Mimari: **[MIMARI.md](MIMARI.md)** · Testler ve sınırlar: **[RAPOR.md](RAPOR.md)**

## Akış

```
Kullanıcı: marka + platform + konu (+ doğrulanmış bilgi, + fotoğraf, + isteğe bağlı tasarım seçimi)
   │
   ▼
AGENT 1 · Content & Design Planner   (agent/planner.py + agent/design.py · Gemini)
   1. Niyet, post türü, hedef kitle
   2. Gerekirse kısa soru (etkinlikte tarih/saat/yer, başarı duyurusunda doğrulanmış sonuç) — genel postta soru yok
   3. TASARIM SEÇİMİ: markanın 8 kompozisyon ailesi arasından konuya, içerik yoğunluğuna ve görsel ihtiyaca göre seçim;
      son kullanılan kompozisyonlar hatırlanır, eşit uygunlukta farklı olan tercih edilir; 2–3 farklı yerleşimli alternatif
   4. Başlık, içerik, CTA, caption, hashtag (Brand Kit dili)
   5. Denetim: karakter sınırı, uydurma sayı/tarih/okul, kopya cümle, tekrar, yasaklı vaat, dil + şablona sığma ölçümü (PNG yazmadan)
   6. Tasarım planı: kompozisyon, gerekçe, sayfa rolleri, görünüm teması, renk, font, logo, fotoğraf kullanımı
   │
   ▼  plan JSON (approval: pending)
KULLANICI · onayla / geri bildirim ver / "Başka tasarım dene" / görünümü değiştir / metni elle düzenle  (her değişiklik yeni sürüm)
   │
   ▼  onaylı plan JSON (approval.hash = içeriğin SHA-256 parmak izi)
AGENT 2 · Visual Production   (agent/producer.py · LLM yok)
   Onayı doğrular → seçilen kompozisyonun HTML/CSS şablonu → PNG (carousel'de tüm sayfalar) → geçmişe kaydeder
```

## Kompozisyon aileleri (her markada 8 Feed + 1 Story)

Her seri gerçekten farklı bir yerleşimdir (renk varyasyonu ayrı şablon sayılmaz). Hepsi Post Kütüphanesi PDF'lerinde belgelidir.

| Marka | Kompozisyonlar |
|---|---|
| ABA Psikoloji | İç Ses (koyu kart) · Ebeveyn Rehberi (soru kutusu) · Mit vs Gerçek (carousel) · Sınav Pasaportu (illüstrasyonlu carousel)* · Haftanın Rutini (adım listesi) · Uzman Notu (bölünmüş editoryal) · **Soru Bandı (renk bantları, fotoğraf yuvası)** · **Alıntı Kartı (ortalanmış, fotoğraf yuvası)** |
| ABA Eğitim | Kabul Duyurusu (dev sayı)* · Son Tarih (takvim)* · Sınav Programı (dev başlık) · “Keşke” Listesi (carousel) · Sayılarla (istatistik kartları)* · Uzman Serisi · **Slogan (ortalanmış tipografi)** · **Fotoğraflı Duyuru (tam sayfa görsel)** |
| Education for Innovation | Program Spotlight* · Playbook (carousel) · Future Careers · Global Network (şehir ızgarası) · Study Smarter · Manifesto · **Process Infographic (ikonlu akış)** · **Innovation Spotlight (büyük görsel)** |
| Design House Global | Portfolio Lesson · Studio Notes · Destinations (carousel) · Six Paths (pastel ızgara) · By the Numbers · Build Your Future · **Service Block (web sitesi bölünmüş blok)** · **Badge Lesson (rozet)** |
| Dört marka · Story | Instagram Story 1080×1920 |

\* Doğrulanmış bilgi gerektirir; bilgi verilmezse seçilmez. Kalın olanlar bu sürümde eklenen kompozisyon aileleridir.
Kompozisyon bilgisi (yerleşim tipi, uygun içerik, fotoğraf kullanımı): `agent/series.py › FAMILY`.

**Görünüm temaları** (her markada 3, Brand Kit paleti içinde) ikincil bir seçenektir; kompozisyonun yerine geçmez.

**Fotoğraf:** Agent görsel üretmez (ücretli API yok). Fotoğraf yuvası olan kompozisyonlarda kullanıcının yüklediği, kullanım hakkı
olan fotoğraf tasarımın parçası olur; fotoğraf yoksa marka grafikleriyle tamamlanır (boş alan kalmaz).

## Onay ve marka kimliği

- `VisualProducer.produce()` onaysız planı ve onaydan sonra değiştirilmiş planı reddeder (`ApprovalError`); kullanıcının vermediği
  sayı/tarih içeren plan onaylanamaz.
- Plan yalnızca metin taşır; logo, renk, font ve iletişim bandı şablon kodundadır. Agent 2 metni yeniden temizler.

## Plan JSON yapısı (Agent 1 → Agent 2)

```json
{
  "schema": "brandpostagent/plan@1", "plan_id": "a1b2c3d4e5f6", "version": 2, "status": "ready",
  "brand": "e4i", "platform": "instagram_feed", "size": [1080, 1350], "language": "en",
  "topic": "…", "facts": "…", "answers": {},
  "analysis": {"intent": "…", "post_type": "info", "series": "process", "reason": "…", "design_reason": "…", "recent": ["field"]},
  "series": "process", "series_name": "Process Infographic", "kind": "single", "theme": "mor",
  "composition": {"series": "process", "layout": "ikonlu-infografik", "desc": "…", "photo": "yok", "preview": "templates/previews/e4i/process.png"},
  "alternatives": [{"series": "spotlight", "layout": "büyük-görsel", "desc": "…"}, {"series": "playbook", "layout": "carousel-adım", "desc": "…"}],
  "content": {"fields": {"…": "…"}, "caption": "…", "hashtags": ["#E4I", "…"]},
  "design": {"format": "Tek post", "size": "1080×1350", "composition": "…", "theme": "Mor gradyan", "pages": [], "colors": [], "fonts": [], "logo": "…"},
  "checks": {"rounds": [], "remaining_warnings": []},
  "feedback_history": [{"type": "design", "text": "Bunu infografik yap", "series": "process", "version": 2}],
  "approval": {"status": "approved", "by": "kullanıcı (arayüz)", "at": "2026-10-23T10:10:00", "hash": "sha256…"}
}
```

Onaylı plan komut satırından da üretilebilir: `python -m agent.producer plan_onayli.json`.

## Klasör yapısı

```
app.py                Streamlit arayüzü
ornekler_uret.py      Örnek üretici (her marka 4 Feed + 1 Story, otomatik tasarım seçimi, her biri kullanıcı onayıyla)
agent/
  planner.py          AGENT 1: niyet, sorular, tasarım seçimi, içerik, denetim, tasarım planı, geri bildirim, tasarım değiştirme
  design.py           Aday sıralama, alternatifler, çeşitlilik geçmişi
  series.py           Seri şemaları + kompozisyon aileleri (FAMILY)
  approval.py         Kullanıcı onayı (SHA-256)
  producer.py         AGENT 2: onaylı plan → PNG
  platforms.py        Instagram Feed / Story (LinkedIn için hazır, kapalı)
  themes.py           Görünüm temaları
  prompts.py, validate.py, llm.py, render.py, render_worker.py, config.py
knowledge/            Marka profilleri: Brand Kit + Post Kütüphanesi bilgi tabanı (JSON)
templates/            HTML/CSS tasarım motoru: engine.py, brands/<marka>.py (şablonlar, temalar, kütüphane metadata'sı),
                      previews/ (tasarım alternatifi önizlemeleri), fonts, assets (logolar)
referans/             Brand Kit ve Post Kütüphanesi PDF'leri
araclar/              onizleme_uret.py (önizlemeleri yeniden üretir)
tests/                run_tests.py (35), app_smoke.py (15), cesitlilik_testi.py (tasarım çeşitliliği) + karşılaştırma görselleri
ornekler/             Gerçek Gemini ile üretilecek örnekler (ornekler_uret.bat)
```

## Komut satırı (isteğe bağlı)

```bash
streamlit run app.py                 # arayüz
python ornekler_uret.py              # örnekler (onaylı)
python -m tests.run_tests            # agent testleri
python -m tests.app_smoke            # arayüz akış testi
python -m tests.cesitlilik_testi     # tasarım çeşitliliği testi
```
