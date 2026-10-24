"""Gemini için istemler. Marka bilgisi knowledge/<marka>.json dosyasından gelir."""
import json, re
from .series import schema_doc, family

LANG = {"tr": "Türkçe", "en": "English (İngilizce)"}
META_ID = {"ic_ses": "01", "ebeveyn": "02", "mit": "03", "rutin": "05", "keske": "04", "sinav": "03", "son_tarih": "02", "kabul": "01",
           "playbook": "02", "field": "03", "study": "05", "manifesto": "06", "program": "01",
           "lesson": "01", "statement": "02", "destinations": "03", "future": "06",
           "pasaport": "04", "soru_bant": "07", "alinti": "08", "veri": "05", "slogan": "07", "foto_duyuru": "08",
           "cities": "04", "process": "07", "spotlight": "08", "paths": "04", "numbers": "05", "service": "07", "badge": "08", "story": "09"}


def series_meta(kb, series):
    mid = META_ID.get(series.id) if series.id != "uzman" else "06"
    if series.id == "rutin" and kb.get("brand") != "aba_psikoloji": mid = None
    return next((x for x in kb["library"]["series"] if x["id"] == mid), None)


def example_for(series):
    """Kütüphane örneği. Doğrulanmış bilgi isteyen serilerde örnekteki sayı, tarih ve okul adları gizlenir;
    böylece model örnekteki gerçek sonuçları (ör. 221) kopyalayamaz."""
    ex = series.example
    if not series.needs_facts:
        return json.dumps(ex, ensure_ascii=False)
    ex = json.loads(json.dumps(ex, ensure_ascii=False))
    for k in getattr(series, "fact_lists", []):
        if k in ex: ex[k] = ["<kullanıcının verdiği okul>"]
    def mask(v):
        if isinstance(v, dict): return {k: mask(x) for k, x in v.items()}
        if isinstance(v, list): return [mask(x) for x in v]
        return re.sub(r"\d+", "<sayı>", v) if isinstance(v, str) else v
    return json.dumps(mask(ex), ensure_ascii=False) + "\n(Köşeli parantezli yerler yalnızca KULLANICININ DOĞRULANMIŞ BİLGİSİYLE doldurulur.)"


def brand_brief(kb):
    v, c = kb["voice"], kb["caption"]
    lines = [
        f"MARKA: {kb['name']} ({kb['handle']}) — {kb['summary']['statement']}",
        f"Hakkında: {kb['summary']['about']}",
        f"Ailedeki rolü: {kb['summary']['role']}",
        f"İÇERİK DİLİ: {v['intro']}",
        "Ses ilkeleri: " + "; ".join(f"{a}: {b}" for a, b in v["pillars"]),
        "İmza kalıplar: " + "; ".join(f"{a} → {b}" for a, b in v["patterns"]),
        "Hitap: " + "; ".join(f"{a}: '{b}' (ör. {c_})" for a, b, c_ in v["address"]),
        "YAP: " + "; ".join(v["do"]),
        "YAPMA: " + "; ".join(v["dont"]),
        "Caption yapısı: " + " → ".join(f"{a} ({b})" for a, b in c["steps"]),
        "Örnek gerçek caption: " + " / ".join(c["example"]),
        "Hashtag havuzu: " + " ".join(c["hashtags"]),
        "Emoji kuralı: " + c["emoji"],
        "Kanca kalıpları: " + " | ".join(kb["library"]["hooks"]),
        "CTA kalıpları: " + " | ".join(kb["library"]["ctas"]),
        "Paylaşmadan önce kontrol listesi: " + " | ".join(kb["checklist"]),
        "DOĞRULANMIŞ MARKA BİLGİLERİ (yalnızca bunlar ve kullanıcının verdiği bilgiler kullanılabilir; 'Instagram paylaşımı:' ile başlayanlar "
        "markanın GEÇMİŞ sonuçlarıdır, yeni bir sonuç / kabul duyurusunda sayı olarak KULLANILMAZ): " + " | ".join(kb["verified_facts"]),
    ]
    return "\n".join(lines)


RULES = """KESİN KURALLAR
1. İstatistik, yüzde, kabul sayısı, tarih, fiyat, kontenjan, ödül, kurum adı UYDURMA. Sayısal veya olgusal bilgiyi yalnızca
   'DOĞRULANMIŞ MARKA BİLGİLERİ' ya da kullanıcının 'doğrulanmış bilgi' alanından al. Emin değilsen sayısız yaz.
2. Gerçek kişilere söz/alıntı atfetme. Uzman veya öğrenci adı uydurma.
3. Her metin alanı verilen karakter sınırının ALTINDA kalmalı; sığmayan metin görselde taşar.
4. İçerik dili: {lang}. Markanın ses tonuna, hitap kuralına ve kalıplarına sadık kal. Görsel metinleri kısa ve vurucu olsun.
5. Konu marka için uygunsuzsa (zarar verici, yanıltıcı, alakasız) markanın diline uygun güvenli bir açıya çevir.
6. Aynı ifadeyi postta iki kez kullanma; şablonun sabit etiketini (seri adı, üst etiket) kapanış cümlesi olarak tekrarlama.
   Her alan yeni bir bilgi ya da eylem eklemeli.
7. Yalnızca istenen JSON nesnesini döndür."""


POST_TYPES = {
    "info": "genel bilgilendirme / ipucu / farkındalık (ek bilgi gerekmez)",
    "event": "etkinlik, seminer, webinar, açık gün, fuar duyurusu (tarih, saat, yer gerekir)",
    "achievement": "gerçek başarı, kabul, sonuç duyurusu (doğrulanmış bilgi gerekir)",
    "deadline": "son başvuru / kayıt tarihi hatırlatması (tarih gerekir)",
    "program": "kurumun bir programını, hizmetini veya kursunu tanıtma",
}


def analyze_prompt(kb, series_list, topic, facts, platform_name, themes=None, recent=None, photo=False):
    """Agent 1, adım 1: niyeti anlar, eksik bilgiyi belirler ve seriyi seçer (tek Gemini çağrısı)."""
    opts = []
    for s in series_list:
        meta = series_meta(kb, s)
        when = meta["when"] if meta else ("Instagram Story: tek ekranlık hızlı mesaj" if s.kind == "story" else "")
        lock = f" [KULLANILAMAZ: {s.needs_facts} gerekli ama verilmedi]" if (s.needs_facts and not facts.strip()) else (f" [gerekli bilgi: {s.needs_facts}]" if s.needs_facts else "")
        kind = {"carousel": "kaydırmalı", "story": "story"}.get(s.kind, "tek post")
        f = family(s)
        opts.append(f"- id='{s.id}' · {s.name} · {kind} · Kompozisyon [{f['layout']}]: {f['desc']} · Uygun içerik: {f['use']} · "
                    f"Fotoğraf: {f['photo']} · Ne zaman: {when}{lock}")
    types = "\n".join(f"- {k}: {v}" for k, v in POST_TYPES.items())
    theme_txt = ", ".join(f"'{k}' = {v}" for k, v in (themes or {}).items()) or "(tema yok)"
    recent_txt = ", ".join(f"{h.get('series')} [{h.get('layout')}]" for h in (recent or [])) or "(henüz yok)"
    system = ("Sen bir sosyal medya içerik stratejistisin. Kullanıcının ne istediğini anlar, gerçekten eksik olan bilgiyi belirler "
              "ve markanın post kütüphanesinden konuya en uygun seriyi seçersin.\n\n" + brand_brief(kb))
    user = f"""PLATFORM: {platform_name}
KONU / KULLANICI İSTEĞİ: {topic}
DOĞRULANMIŞ BİLGİ VE KULLANICI YANITLARI: {facts or '(yok)'}

POST TÜRLERİ:
{types}

KÜTÜPHANEDEKİ SERİLER:
{chr(10).join(opts)}

1) Kullanıcının niyetini tek cümleyle yaz ve post türünü seç.
2) Yalnızca postu doğru yazmak için GERÇEKTEN gerekli olup verilmemiş bilgileri soru olarak yaz (en fazla 3, kısa, Türkçe).
   Genel bilgilendirici postlarda soru sorma. Var olan bilgiyi tekrar sorma.
3) KULLANILAMAZ işaretli olmayan seriler arasından içeriğe en uygun KOMPOZİSYONU seç. İlk listedeki seriyi otomatik seçme;
   konunun amacına, içerik yoğunluğuna (tek fikir mi, adımlar mı, sayı mı, soru mu) ve görsel ihtiyacına bak.
   SON KULLANILAN KOMPOZİSYONLAR (bu marka, yeniden eskiye): {recent_txt}
   İçeriğe eşit derecede uygun seçenekler varsa son kullanılanlardan FARKLI kompozisyonu tercih et; ama içerik uygunluğu ve marka
   kimliği çeşitlilikten önce gelir. Kullanıcı fotoğraf {'YÜKLEDİ' if photo else 'yüklemedi'}.
   Ayrıca bu konu için gerçekten uygun, birbirinden FARKLI kompozisyonda 2 alternatif seri öner.
4) Konunun duygusuna uygun görünüm (zemin) temasını seç: {theme_txt}
JSON: {{"intent": "<niyet, 1 cümle, Türkçe>", "post_type": "<{'|'.join(POST_TYPES)}>", "questions": ["<soru>", ...],
 "series": "<id>", "reason": "<neden bu seri, 1-2 cümle, Türkçe>", "angle": "<postun ana fikri, 1 cümle>", "audience": "<öğrenci/veli/genel/kurum>",
 "theme": "<tema id>", "alternatives": ["<id>", "<id>"], "design_reason": "<bu kompozisyonun neden uygun olduğu, 1 cümle, Türkçe>"}}"""
    return system, user


def write_prompt(kb, series, topic, facts, plan, platform_name="Instagram Feed"):
    lang = LANG[kb["language"]]
    meta = series_meta(kb, series)
    slots = "\n".join("- " + s for s in (meta["slots"] if meta else []))
    system = "Sen bu markanın kıdemli sosyal medya metin yazarısın. Post kütüphanesindeki şablonu doldurursun.\n\n" + brand_brief(kb) + "\n\n" + RULES.format(lang=lang)
    story = series.kind == "story"
    cap_rule = ("Instagram Story'de caption görünmez. 'caption' alanına story'nin öne çıkanlara eklenirken ya da akışta paylaşılırken "
                f"kullanılacak 1-2 cümlelik kısa not yaz ({lang}). Hashtag: 1-3 adet (story hashtag çıkartması), ilki markanın etiketi."
                if story else
                f"Ayrıca Instagram caption'ı yaz: markanın caption yapısına uy, {lang}, 3-6 kısa paragraf, en fazla 900 karakter, hashtag'leri caption'a yazma.\n"
                "Hashtag: 5-7 adet, ilki markanın etiketi.")
    user = f"""PLATFORM: {platform_name}
KONU: {topic}
DOĞRULANMIŞ BİLGİ (kullanıcı): {facts or '(yok)'}
SEÇİLEN SERİ: {series.name} ({ {'carousel': 'kaydırmalı', 'story': 'story, tek ekran 1080×1920'}.get(series.kind, 'tek post') })
ANA FİKİR: {plan.get('angle', '')}
HEDEF KİTLE: {plan.get('audience', '')}

Serinin şablon yapısı (kütüphaneden):
{slots}

DOLDURULACAK ALANLAR (sınırlar görünen karakter sayısıdır):
{schema_doc(series.schema)}

Bu serinin kütüphanedeki örneği (yapıyı ve tonu örnek al, metni KOPYALAMA, konuya göre yeniden yaz):
{example_for(series)}

{cap_rule}

JSON:
{{"fields": {{...yukarıdaki alanlar...}}, "caption": "...", "hashtags": ["#...", ...],
 "self_check": [{{"rule": "<kontrol listesinden madde>", "ok": true, "note": "..."}}]}}"""
    return system, user


def review_prompt(kb, series, draft):
    system = "Sen markanın Brand Kit denetçisisin. Taslağı yalnızca markanın kurallarına göre değerlendirirsin.\n\n" + brand_brief(kb)
    user = f"""SERİ: {series.name}
TASLAK:
{json.dumps(draft, ensure_ascii=False)}

Taslağı kontrol listesi, ses tonu, hitap kuralı, YAP/YAPMA ve doğrulanmış bilgi kuralına göre değerlendir.
Yalnızca GERÇEK ihlalleri yaz; zevk meselesi önerileri yazma.
JSON: {{"score": <0-10>, "issues": ["<somut ihlal ve nasıl düzeltileceği>", ...], "summary": "<1 cümle, Türkçe>"}}"""
    return system, user


def revise_prompt(kb, series, draft, issues, topic, facts):
    lang = LANG[kb["language"]]
    system = "Sen bu markanın kıdemli sosyal medya metin yazarısın. Denetimden dönen taslağı düzeltirsin.\n\n" + brand_brief(kb) + "\n\n" + RULES.format(lang=lang)
    user = f"""KONU: {topic}
DOĞRULANMIŞ BİLGİ (kullanıcı): {facts or '(yok)'}
SERİ: {series.name}
ALANLAR VE SINIRLAR:
{schema_doc(series.schema)}

MEVCUT TASLAK:
{json.dumps(draft, ensure_ascii=False)}

DÜZELTİLMESİ GEREKEN SORUNLAR:
{chr(10).join('- ' + i for i in issues)}

Sorunların hepsini düzelt, geri kalanı koru. Aynı JSON yapısında TAMAMINI döndür:
{{"fields": {{...}}, "caption": "...", "hashtags": [...], "self_check": [...]}}"""
    return system, user


def feedback_prompt(kb, series, draft, feedback, topic, facts, platform_name="Instagram Feed", options=None):
    """Agent 1: kullanıcının geri bildirimine göre planı günceller."""
    lang = LANG[kb["language"]]
    opt_txt = "\n".join(f"- id='{o.id}' · {o.name} · [{family(o)['layout']}] {family(o)['desc']}" for o in (options or []) if o.id != series.id) or "(yok)"
    system = ("Sen bu markanın kıdemli sosyal medya metin yazarısın. Kullanıcının onayına sunulan taslağı, kullanıcının geri bildirimine göre "
              "güncellersin. Geri bildirim marka kurallarıyla çelişirse (ör. logo, renk, font değişikliği, doğrulanmamış bilgi) o kısmı uygulama "
              "ve 'not' alanında kısaca açıkla.\n\n" + brand_brief(kb) + "\n\n" + RULES.format(lang=lang))
    user = f"""PLATFORM: {platform_name}
KONU: {topic}
DOĞRULANMIŞ BİLGİ (kullanıcı): {facts or '(yok)'}
SERİ: {series.name}
ALANLAR VE SINIRLAR:
{schema_doc(series.schema)}

KULLANICIYA SUNULAN TASLAK:
{json.dumps(draft, ensure_ascii=False)}

KULLANICININ GERİ BİLDİRİMİ:
{feedback}

KULLANILABİLİR DİĞER TASARIMLAR (aynı marka):
{opt_txt}

Kullanıcı açıkça farklı bir tasarım / format / kompozisyon istiyorsa (ör. "infografik yap", "carousel olarak anlat", "daha minimal",
"fotoğraf ağırlıklı", "başka tasarım dene") 'switch_series' alanına yukarıdaki listeden en uygun seri id'sini yaz; bu durumda alanları
doldurmana gerek yok. Yalnızca metin değişikliği istiyorsa 'switch_series' boş kalsın ve geri bildirimi uygula.
JSON: {{"switch_series": "<id ya da boş>", "fields": {{...}}, "caption": "...", "hashtags": [...], "self_check": [...],
 "not": "<uygulanamayan istek varsa kısa açıklama, yoksa boş>"}}"""
    return system, user
