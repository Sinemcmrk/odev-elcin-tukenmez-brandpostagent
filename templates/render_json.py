"""JSON'dan Instagram postu üretir.

Kullanım:
    python render.py examples/aba_psikoloji.json            # dosyadaki tüm postlar
    python render.py examples/aba_psikoloji.json ic-ses     # adı bununla başlayanlar

JSON biçimi:
{
  "brand": "aba_psikoloji",            # aba_psikoloji | aba_egitim | e4i | design_house
  "out": "cikti/aba_psikoloji",        # PNG klasörü (isteğe bağlı)
  "logo": "assets/aba-psikoloji/logo-mark-white.png",   # logo değiştirmek için (isteğe bağlı)
  "posts": [
    {"name": "01-ic-ses", "template": "ic_ses",
     "data": {"tag": "...", "quote": ["...", "..."], "label": "...", "body": "...", "cta": "..."},
     "photo": "foto.jpg", "photo_opacity": 0.3,       # fotoğraf isteğe bağlı
     "theme": "koyu"}                                  # görünüm teması isteğe bağlı (markanın THEMES sözlüğü)
  ]
}
"""
import sys, json, importlib, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "brands"))
import engine

TEMPLATES = {
    "aba_psikoloji": ["ic_ses", "ebeveyn", "mit_kapak", "mit_sayfa", "kapanis", "pasaport_kapak", "pasaport_ic", "pasaport_son", "rutin", "uzman", "soru_bant", "alinti", "story"],
    "aba_egitim": ["kabul", "son_tarih", "sinav", "keske_kapak", "keske_sayfa", "keske_son", "veri", "uzman", "slogan", "foto_duyuru", "story"],
    "e4i": ["program", "play_cover", "play_step", "field", "cities", "study", "manifesto", "process", "spotlight", "story"],
    "design_house": ["lesson", "statement", "dest_cover", "dest_city", "paths", "numbers", "future", "service", "badge", "story"],
}
LOGO_VAR = {"aba_psikoloji": "LOGO", "aba_egitim": "LOGO", "e4i": "LOGO", "design_house": "MONO"}

def build(spec, only=None):
    brand = spec["brand"]
    m = importlib.import_module(brand)
    if spec.get("logo"):
        setattr(m, LOGO_VAR[brand], engine._src(str((ROOT / spec["logo"]) if not spec["logo"].startswith(("http", "file")) else spec["logo"])))
    items = []
    for p in spec["posts"]:
        if only and not p["name"].startswith(only): continue
        if p["template"] not in TEMPLATES[brand]:
            raise SystemExit(f"Bilinmeyen şablon: {p['template']} (seçenekler: {', '.join(TEMPLATES[brand])})")
        data = dict(p["data"])
        slot = p["template"] in getattr(m, "PHOTO_SLOT", ())
        if slot and p.get("photo"):
            data["photo"] = engine._src(str(ROOT / p["photo"]) if not p["photo"].startswith(("http", "file", "/")) else p["photo"])
        html = getattr(m, p["template"])(data)
        theme = p.get("theme") or spec.get("theme")          # isteğe bağlı görünüm teması (THEMES sözlüğü)
        if theme and p["template"] not in getattr(m, "NO_THEME", ()):
            html = engine.with_theme(html, theme, getattr(m, "THEMES", {}))
        if p.get("photo") and not slot:
            html = engine.with_photo(html, p["photo"], p.get("photo_opacity", 0.3), p.get("photo_blend", "luminosity"))
        items.append((p["name"], html))
    out = spec.get("out") or f"cikti/{brand}"
    engine.render(items, str(ROOT / out))
    print(f"{len(items)} post → {out}")

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    build(spec, sys.argv[2] if len(sys.argv) > 2 else None)
