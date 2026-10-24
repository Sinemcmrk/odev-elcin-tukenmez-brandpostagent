"""Kurala dayalı (deterministik) Brand Kit denetimi.

LLM'in ürettiği içerik şablona girmeden önce burada kontrol edilir:
alan yapısı ve karakter sınırları, izin verilen HTML, doğrulanmamış sayı/tarih,
yasaklı vaatler, caption ve hashtag kuralları, içerik dili.
"""
import html, re
from .series import S, L, O

ALLOWED_TAGS = [r"<b>", r"</b>", r"<br>", r"<br/>", r"<br />", r"<em>", r"</em>", r"<i>", r"</i>",
                r"<span class='o'>", r'<span class="o">', r"<span class='l'>", r'<span class="l">', r"</span>"]
BANNED = {
    "tr": ["garanti", "kesin çözüm", "kesin kabul", "%100", "yüzde yüz", "mucize", "kanıtlanmış"],
    "en": ["guarantee", "guaranteed", "100%", "miracle", "never fail", "proven"],
}
BRAND_TAG = {"aba_psikoloji": "#ABAPsikoloji", "aba_egitim": "#ABAEğitim", "e4i": "#E4I", "design_house": "#DesignHouseGlobal"}
MONTHS = r"(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık|january|february|march|april|may|june|july|august|september|october|november|december)"
TR_CHARS = set("çğıöşüÇĞİÖŞÜ")


def visible(s):
    return re.sub(r"<[^>]+>", "", s or "")


def sanitize(s, allow_html):
    """HTML'i kaçırır; yalnızca şablonların beklediği küçük etiket kümesine izin verir."""
    s = html.unescape(str(s or "").strip())      # idempotent: önceden temizlenmiş metin iki kez kaçırılmaz (&amp;amp;)
    out = html.escape(s, quote=False)
    if allow_html:
        for t in ALLOWED_TAGS:
            out = out.replace(html.escape(t, quote=False), t)
    return out


def check_schema(schema, fields, path=""):
    """Alanları şemaya göre temizler; (temiz_alanlar, sorunlar) döndürür."""
    issues, clean = [], {}
    if not isinstance(fields, dict):
        return {}, [f"{path or 'fields'}: nesne bekleniyordu"]
    for k, spec in schema.items():
        p = f"{path}{k}"
        v = fields.get(k)
        if isinstance(spec, S):
            if v is None or str(v).strip() == "":
                if spec.req: issues.append(f"{p}: boş bırakılmış, doldurulmalı")
                clean[k] = ""; continue
            if isinstance(v, list): v = " ".join(map(str, v))
            n = len(visible(str(v)))
            if n > spec.max:
                issues.append(f"{p}: {n} karakter, en fazla {spec.max} olmalı (kısalt)")
            clean[k] = sanitize(v, spec.html)
        elif isinstance(spec, L):
            if not isinstance(v, list):
                issues.append(f"{p}: liste olmalı"); clean[k] = []; continue
            if not (spec.min <= len(v) <= spec.max):
                issues.append(f"{p}: {len(v)} öğe var, {spec.min}–{spec.max} öğe olmalı")
            items = []
            for i, it in enumerate(v[:spec.max]):
                if isinstance(spec.item, O):
                    c, iss = check_schema(spec.item.fields, it, f"{p}[{i+1}].")
                elif isinstance(spec.item, L):
                    c, iss = check_schema({"x": spec.item}, {"x": it}, f"{p}[{i+1}]")
                    c = c.get("x", [])
                else:
                    c, iss = check_schema({"x": spec.item}, {"x": it}, f"{p}[{i+1}]")
                    c = c.get("x", "")
                items.append(c); issues += [x.replace(".x", "").replace("]x", "]") for x in iss]
            clean[k] = items
        elif isinstance(spec, O):
            c, iss = check_schema(spec.fields, v or {}, p + ".")
            clean[k] = c; issues += iss
    return clean, issues


def all_text(x):
    if isinstance(x, dict): return " ".join(all_text(v) for v in x.values())
    if isinstance(x, (list, tuple)): return " ".join(all_text(v) for v in x)
    return visible(str(x))


PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s.()-]*)?\(?\d{3}\)?[\s.-]*\d{3}[\s.-]*\d{2}[\s.-]*\d{2}")


def check_facts(text, allowed_sources):
    """Kaynaklarda geçmeyen yüzde, yıl, büyük sayı ve tarihleri işaretler. Telefon numaraları sayı sayılmaz."""
    issues = []
    text = PHONE_RE.sub(" ", text or "")
    allowed = allowed_sources.lower()
    for m in re.finditer(r"(\d+(?:[.,]\d+)*)\s*(%|\+)?", text):
        num, suf = m.group(1), m.group(2) or ""
        if num in allowed:
            continue
        val = float(num.replace(".", "").replace(",", ".")) if num.replace(".", "").replace(",", "").isdigit() else 0
        pre = text[max(0, m.start() - 1):m.start()]
        if suf == "%" or pre == "%" or re.fullmatch(r"(19|20)\d\d", num) or val >= 13:
            issues.append(f"Doğrulanmamış sayı/istatistik: “{m.group(0).strip()}”. Kullanıcı ya da marka bilgilerinde yok; kaldır veya sayısız ifade et.")
    for m in re.finditer(r"\b\d{1,2}\s+" + MONTHS, text.lower()):
        if m.group(0) not in allowed:
            issues.append(f"Doğrulanmamış tarih: “{m.group(0)}”. Tarih yalnızca kullanıcı verdiyse kullanılabilir.")
    return list(dict.fromkeys(issues))


def _norm(t):
    return re.sub(r"[^\wçğıöşü ]", "", visible(t).lower()).strip()


def check_repeats(fields, fixed_labels=()):
    """Aynı ifadenin iki alanda ya da şablonun sabit etiketinde tekrar edilmesini yakalar."""
    texts, issues = [], []
    def walk(x, path):
        if isinstance(x, dict):
            for k, v in x.items(): walk(v, f"{path}{k}.")
        elif isinstance(x, list):
            for i, v in enumerate(x): walk(v, f"{path}{i+1}.")
        elif isinstance(x, str):
            parts = [_norm(t) for t in re.split(r"[+·•,/|]| ve | and ", visible(x)) if _norm(t)]
            dup = {t for t in parts if parts.count(t) > 1}
            if len(parts) > 1 and dup:
                issues.append(f"{path.rstrip('.')}: “{', '.join(sorted(dup))}” aynı alanda iki kez yazılmış; farklı bir öğeyle değiştir.")
            if len(_norm(x)) >= 10:
                texts.append((path.rstrip("."), _norm(x)))
    walk(fields, "")
    labels = [_norm(l) for l in fixed_labels]
    for i, (p1, t1) in enumerate(texts):
        for p2, t2 in texts[i + 1:]:
            if t1 == t2:
                issues.append(f"{p1} ve {p2} aynı ifadeyi tekrarlıyor; birini yeni bir bilgi ya da eylemle değiştir.")
        for l in labels:
            if t1 in l:
                issues.append(f"{p1}: şablonun sabit etiketini (“{l}”) tekrarlıyor; farklı bir kapanış cümlesi yaz.")
    return issues


FACT_MARKERS = ("Doğrulanmamış",)


def blocking(warnings):
    """Onayı engelleyen uyarılar: doğrulanmamış sayı, istatistik ya da tarih."""
    return [w for w in warnings or [] if w.startswith(FACT_MARKERS)]


def _texts(x, path=""):
    if isinstance(x, dict):
        for k, v in x.items(): yield from _texts(v, f"{path}{k}.")
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from _texts(v, f"{path}{i+1}.")
    elif isinstance(x, str):
        yield path.rstrip("."), x


def check_copy(series, fields):
    """Kütüphane örneğinden kelimesi kelimesine kopyalanan cümleleri yakalar (her post aynı görünmesin diye)."""
    ex = {_norm(t) for _, t in _texts(getattr(series, "example", {})) if len(_norm(t)) >= 22}
    skip = ("cta", "tag", "lab", "btn")   # CTA ve etiketler markanın imza kalıplarıdır; tekrar etmeleri doğaldır
    return [f"{p}: “{visible(t)[:50]}” kütüphane örneğiyle aynı. Örneği kopyalama; konuya özgü yeni bir cümle yaz."
            for p, t in _texts(fields) if _norm(t) in ex and not any(k in p.split(".")[0] for k in skip)]


# Design House'un web sitesinde listelenen hedef okullar ve kısaltmaları (Destinations serisinde yalnızca bunlar)
DH_ALIASES = {"csm": "central saint martins", "rca": "royal college of art", "risd": "rhode island school of design",
              "ual": "university of the arts london", "sva": "school of visual arts", "dae": "design academy eindhoven"}


def check_schools(series, fields, brand_facts):
    if getattr(series, "id", "") != "destinations":
        return []
    known = " ".join(brand_facts).lower()
    out = []
    for i, c in enumerate(fields.get("cities") or []):
        for name in re.split(r"\+|,|&| and ", visible(str(c.get("schools", "")).replace("<br>", " "))):
            n = re.sub(r"[^\w ]", "", name).strip().lower()
            n = DH_ALIASES.get(n, n)
            if n and n not in known:
                out.append(f"cities[{i+1}].schools: “{name.strip()}” Design House'un web sitesindeki okul listesinde yok; yalnızca listedeki okulları kullan.")
    return out


def check_post(brand, lang, series, fields, caption, hashtags, topic, facts, brand_facts):
    story = getattr(series, "kind", "") == "story"
    max_tags, min_tags = (3, 1) if story else (8, 4)
    clean, issues = check_schema(series.schema, fields)
    fixes = []
    body_text = all_text({k: v for k, v in clean.items() if k != "tr"})
    # Doğrulanmış bilgi isteyen serilerde (kabul, son tarih, program) sayı ve tarih YALNIZCA kullanıcının bilgisinden gelir;
    # markanın geçmiş paylaşımlarındaki sonuçlar (ör. "221 öğrenci") yeni bir duyuruda kullanılamaz.
    strict = bool(getattr(series, "needs_facts", None))
    usable = [f for f in brand_facts if not (strict and f.startswith("Instagram paylaşımı"))]
    sources = " ".join([topic or "", facts or ""] + usable)
    for lf in getattr(series, "fact_lists", []):
        keep = [x for x in (clean.get(lf) or []) if visible(str(x)).strip().lower() in (facts or "").lower()]
        dropped = [visible(str(x)) for x in (clean.get(lf) or []) if x not in keep]
        if dropped:
            clean[lf] = keep
            fixes.append(f"{lf}: kullanıcının bilgisinde geçmeyen öğeler çıkarıldı ({', '.join(dropped)}).")
    issues += check_facts(body_text + " " + (caption or ""), sources)
    low = (body_text + " " + (caption or "")).lower()
    for w in BANNED[lang]:
        if w in low:
            issues.append(f"Yasaklı vaat ifadesi: “{w}”. Brand Kit 'yapma' kuralı; kaldır.")
    if lang == "en" and any(ch in TR_CHARS for ch in body_text + (caption or "")):
        issues.append("İçerik İngilizce olmalı; Türkçe karakterli kelimeler var (yalnızca 'tr' alanı Türkçe olabilir).")
    issues += check_repeats(clean, getattr(series, "fixed_labels", []))
    issues += check_copy(series, clean)
    issues += check_schools(series, clean, brand_facts)
    cap = (caption or "").strip()
    if not cap:
        issues.append("caption boş")
    elif len(cap) > 2000:
        issues.append(f"caption {len(cap)} karakter; 2000'in altına indir")
    tags = []
    for t in (hashtags or []):
        t = "#" + re.sub(r"[^\wçğıöşüÇĞİÖŞÜ]", "", str(t).lstrip("#"))
        if len(t) > 1 and t.lower() not in [x.lower() for x in tags]: tags.append(t)
    bt = BRAND_TAG[brand]
    if not tags or tags[0].lower() != bt.lower():
        tags = [bt] + [t for t in tags if t.lower() != bt.lower()]
        fixes.append(f"Marka etiketi {bt} başa alındı.")
    if len(tags) > max_tags:
        tags = tags[:max_tags]; fixes.append(f"Hashtag sayısı {max_tags}'e indirildi.")
    if len(tags) < min_tags:
        issues.append(f"En az {min_tags} hashtag olmalı (şu an {len(tags)}).")
    return clean, cap, tags, issues, fixes


def hard_trim(schema, fields):
    """Son çare: düzeltme turları bittiyse karakter sınırını aşan metni kısaltır."""
    out = {}
    for k, spec in schema.items():
        v = fields.get(k)
        if isinstance(spec, S) and isinstance(v, str) and len(visible(v)) > spec.max:
            t = visible(v)[: spec.max - 1].rsplit(" ", 1)[0]
            out[k] = html.escape(t, quote=False) + "…"
        elif isinstance(spec, L) and isinstance(v, list):
            out[k] = [hard_trim(spec.item.fields, x) if isinstance(spec.item, O) else (hard_trim({"x": spec.item}, {"x": x})["x"]) for x in v[:spec.max]]
        else:
            out[k] = v
    return out
