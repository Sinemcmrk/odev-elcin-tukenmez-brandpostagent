"""Tasarım alternatifleri için küçük önizlemeler üretir: templates/previews/<marka>/<seri>.png
Her seri, kütüphane örnek içeriğiyle çizilir (ilk sayfa). Çalıştırma: python -m araclar.onizleme_uret"""
import pathlib, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from PIL import Image
from agent import series as SR
from agent.render import render_pages

OUT = ROOT / "templates" / "previews"
tmp = ROOT / "outputs" / "_onizleme"
for pf, by_brand in SR.PLATFORM_SERIES.items():
    for b, lst in by_brand.items():
        for s in lst:
            t, d = s.build(s.example)[0]
            pngs, _ = render_pages(b, [(s.id, t, d)], tmp)
            im = Image.open(pngs[0]).convert("RGB"); im.thumbnail((360, 640))
            (OUT / b).mkdir(parents=True, exist_ok=True); im.save(OUT / b / f"{s.id}.png", optimize=True)
            print(b, s.id)
shutil.rmtree(tmp, ignore_errors=True)
