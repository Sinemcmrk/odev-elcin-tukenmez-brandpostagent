# Sistem Mimarisi (kısa)

```
┌──────────────┐   istek    ┌────────────────────────────── AGENT 1 (Gemini, ücretsiz) ─────────────────────────────┐
│  Streamlit   │ ─────────▶ │ analiz çağrısı: niyet + tür + soru + kompozisyon seçimi + 2 alternatif + tema           │
│  app.py      │            │ design.py: aday sıralama (içerik uygunluğu, post türü, fotoğraf) + son kompozisyonlar   │
│              │ ◀───────── │ yazım çağrısı → kod denetimi + sığma ölçümü (PNG yok) → gerekirse düzeltme çağrısı      │
│  plan ekranı │   plan     └─────────────────────────────────────────────────────────────────────────────────────────┘
│  · onay      │                     ▲ geri bildirim / "Başka tasarım dene" (yeni sürüm, 1 çağrı)
│  · geri bild.│                     │
│  · tasarım   │   onaylı plan (SHA-256)
│  · görünüm   │ ─────────▶ ┌──────────── AGENT 2 (LLM yok) ────────────┐
│              │            │ onay doğrulama → şablon → Playwright → PNG │ ──▶ outputs/ + tasarım geçmişi
│  indirme     │ ◀───────── └────────────────────────────────────────────┘
└──────────────┘
```

**Bilgi kaynakları:** `knowledge/<marka>.json` (Brand Kit: ses, hitap, YAP/YAPMA, caption yapısı, palet, doğrulanmış bilgiler;
Post Kütüphanesi: seriler, kancalar, CTA'lar) ve `templates/brands/<marka>.py` (şablonlar, temalar, kütüphane metadata'sı).
Post Kütüphanesi PDF'leri de aynı şablon kodundan üretilir; PDF ile agent aynı serileri kullanır.

**Tasarım çeşitliliği nasıl sağlanır?**
1. Her markada 8 farklı yerleşim ailesi (kart, soru kutusu, carousel, bantlar, ortalanmış alıntı, tam sayfa görsel, infografik,
   bölünmüş blok, rozet…). Renk temaları ayrıca vardır ama ayrı tasarım sayılmaz.
2. Agent 1, aileleri açıklamalarıyla görür ve konuya göre seçer; ilk sıradakini otomatik almaz.
3. Son üretilen kompozisyonlar (`outputs/_tasarim_gecmisi.json`) modele verilir; eşit uygunlukta farklı olan seçilir.
4. Her planla birlikte 2–3 farklı yerleşimli alternatif (önizlemeli) sunulur; seçim ek çağrı gerektirmez, uygulaması 1 çağrıdır.
5. Geri bildirimdeki tasarım istekleri ("infografik yap", "carousel olarak anlat") seriyi değiştirir.

**Güvenlik ve doğruluk:** API anahtarı yalnızca `.env`; ücretli servise geçiş yok; sayı/tarih/okul yalnızca kullanıcı ya da doğrulanmış
marka bilgisinden; onay olmadan görsel yok.

**Genişletme:** Yeni platform → `agent/platforms.py`; yeni kompozisyon → `templates/brands/<marka>.py` (şablon) + `agent/series.py`
(şema + FAMILY) + kütüphane META kaydı.
