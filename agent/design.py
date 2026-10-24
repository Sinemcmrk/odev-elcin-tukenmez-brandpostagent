"""Tasarım seçimi: aday kompozisyonları sıralama, alternatif önerme ve çeşitlilik geçmişi.

Öncelik sırası (kullanıcının istediği gibi): 1) marka kimliği, 2) içerik uygunluğu, 3) çeşitlilik.
- Seçimi Gemini yapar (Agent 1'in ilk çağrısı); bu modül ona aday listesi, kompozisyon bilgisi ve son kullanılan
  kompozisyonları verir, ayrıca modelin seçimi geçersizse ya da alternatif gerekirse koddan sıralama yapar.
- Alternatifler ek Gemini çağrısı olmadan, seri metadata'sından (agent/series.py › FAMILY) üretilir.
- Geçmiş: outputs/_tasarim_gecmisi.json — Agent 2'nin ürettiği son postların kompozisyonları.
"""
import datetime, json, pathlib, re
from . import series as SR

ROOT = pathlib.Path(__file__).resolve().parent.parent
HISTORY = ROOT / "outputs" / "_tasarim_gecmisi.json"
PREVIEWS = ROOT / "templates" / "previews"

# Post türüne göre doğal kompozisyonlar (içerik uygunluğu ipucu; kesin kural değil)
TYPE_HINT = {
    "event": {"foto_duyuru", "son_tarih", "program", "spotlight", "slogan", "service"},
    "deadline": {"son_tarih", "foto_duyuru"},
    "achievement": {"kabul", "veri", "numbers"},
    "program": {"sinav", "program", "service", "slogan", "foto_duyuru", "playbook"},
    "info": set(),
}


def _stem(w):
    return w[:5]


def _tokens(text):
    return {_stem(w) for w in re.findall(r"[a-zçğıöşü]{4,}", (text or "").lower())}


def load_history():
    try:
        return json.loads(HISTORY.read_text(encoding="utf-8"))
    except Exception:
        return []


def recent(brand, n=4):
    return [h for h in reversed(load_history()) if h.get("brand") == brand][:n]


def record(brand, series_id, topic):
    ser = None
    for pool in SR.PLATFORM_SERIES.values():
        ser = next((s for s in pool.get(brand, []) if s.id == series_id), ser)
    h = load_history()
    h.append({"brand": brand, "series": series_id, "layout": SR.family(ser)["layout"] if ser else "",
              "topic": topic[:80], "at": datetime.datetime.now().isoformat(timespec="seconds")})
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps(h[-60:], ensure_ascii=False, indent=1), encoding="utf-8")


def score(series, topic, ptype, kb_meta=None, photo=False):
    f = SR.family(series)
    words = _tokens(topic)
    pool = _tokens(" ".join([series.name, f["desc"], f["use"], (kb_meta or {}).get("when", "")]))
    s = len(words & pool) * 1.0
    if series.id in TYPE_HINT.get(ptype, set()):
        s += 1.5
    if photo and f["photo"] != "yok":
        s += 0.75
    return s


def rank(brand, usable, topic, ptype, kb=None, photo=False, history=None):
    """Adayları içerik uygunluğuna göre sıralar; son kullanılan kompozisyonlara küçük bir ceza verir."""
    metas = {m["id"]: m for m in (kb or {}).get("library", {}).get("series", [])}
    from .prompts import META_ID
    hist = history if history is not None else recent(brand)
    last = [h.get("layout") for h in hist]
    out = []
    for s in usable:
        sc = score(s, topic, ptype, metas.get(META_ID.get(s.id, "")), photo)
        lay = SR.family(s)["layout"]
        if last and lay == last[0]:
            sc -= 1.25
        elif lay in last[:3]:
            sc -= 0.5
        out.append((sc, s))
    out.sort(key=lambda x: -x[0])
    return [s for _, s in out]


def alternatives(primary, ranked, wanted=(), k=3):
    """Birincil tasarımdan FARKLI yerleşimli en fazla k alternatif (önce modelin önerdikleri)."""
    by_id = {s.id: s for s in ranked}
    seen, alts = {SR.family(primary)["layout"]}, []
    for s in [by_id[i] for i in wanted if i in by_id] + ranked:
        lay = SR.family(s)["layout"]
        if s.id != primary.id and lay not in seen:
            alts.append(s); seen.add(lay)
        if len(alts) == k:
            break
    return alts


def describe(s):
    f = SR.family(s)
    prev = PREVIEWS / s.brand / f"{s.id}.png"
    return {"series": s.id, "name": s.name, "layout": f["layout"], "desc": f["desc"], "use": f["use"],
            "photo": f["photo"], "kind": s.kind, "preview": str(prev) if prev.exists() else None}
