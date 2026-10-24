"""Ayrı bir süreçte çalışan çizim işçisi (Streamlit + Playwright'ın Windows'ta çakışmaması için).
Kullanım: python -m agent.render_worker istek.json
istek.json: {"brand": "...", "out": "klasör", "pages": [{"name","template","data"}], "photo": null, "photo_opacity": 0.3}
Çıktı: out/_render_report.json  →  {"overflow": {sayfa_adı: [taşan metinler]}}
"""
import sys, json, pathlib, importlib
ROOT = pathlib.Path(__file__).resolve().parent.parent / "templates"
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "brands"))
import engine

def main(path):
    req = json.load(open(path, encoding="utf-8"))
    m = importlib.import_module(req["brand"])
    items = []
    for p in req["pages"]:
        data = dict(p["data"])
        slot = p["template"] in getattr(m, "PHOTO_SLOT", ())
        if slot and req.get("photo"):
            data["photo"] = engine._src(req["photo"])      # fotoğraf yuvası olan şablon: fotoğraf tasarımın parçası
        html = getattr(m, p["template"])(data)
        if req.get("theme") and p["template"] not in getattr(m, "NO_THEME", ()):
            html = engine.with_theme(html, req["theme"], getattr(m, "THEMES", {}))
        if req.get("photo") and not slot:
            html = engine.with_photo(html, req["photo"], req.get("photo_opacity", 0.3))
        items.append((p["name"], html))
    report = engine.render(items, req["out"], req.get("shots", True))
    json.dump({"overflow": report}, open(pathlib.Path(req["out"]) / "_render_report.json", "w", encoding="utf-8"), ensure_ascii=False)

if __name__ == "__main__":
    main(sys.argv[1])
