"""Arayüz görsellerini üretir: marka logosu kutucukları (templates/assets/ui/<marka>.png) ve agent ikonu (agent.png).
Logolar markaların kendi logo dosyalarıdır; yalnızca kare bir zemine yerleştirilir. Çalıştırma: python araclar/ui_gorselleri.py"""
import pathlib
from PIL import Image, ImageDraw
A = pathlib.Path(__file__).resolve().parent.parent / "templates" / "assets"
OUT = A / "ui"; OUT.mkdir(exist_ok=True)
S = 320

def tile(bg, logo, scale, name):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    m = Image.new("L", (S, S), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, S - 1, S - 1), 64, fill=255)
    im.paste(Image.new("RGBA", (S, S), bg), (0, 0), m)
    lg = Image.open(A / logo).convert("RGBA"); lg.thumbnail((int(S * scale), int(S * scale)), Image.LANCZOS)
    im.alpha_composite(lg, ((S - lg.width) // 2, (S - lg.height) // 2))
    im.save(OUT / f"{name}.png")

tile("#F48011", "aba-psikoloji/logo-mark-white.png", .58, "aba_psikoloji")
tile("#06162F", "aba-egitim/logo-mark-white.png", .58, "aba_egitim")
tile("#FFFFFF", "e4i/logo.png", .82, "e4i")
tile("#0B0B0B", "design-house/logo-tile.png", 1.0, "design_house")

# Agent ikonu: koyu zemin, üst üste üç post kartı ve bir kıvılcım (özgün çizim)
k = 4; s = S * k
im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, s - 1, s - 1), 70 * k, fill=255)
bg = Image.new("RGBA", (s, s), "#1B1E2B"); im.paste(bg, (0, 0), m)
def card(x, y, w, h, fill): d.rounded_rectangle((x * k, y * k, (x + w) * k, (y + h) * k), 22 * k, fill=fill)
card(118, 58, 128, 160, "#5E2390")
card(96, 80, 128, 160, "#F95B1C")
card(74, 102, 128, 160, "#FFF7EB")
d.rounded_rectangle((96 * k, 130 * k, 172 * k, 144 * k), 7 * k, fill="#1B1E2B")
d.rounded_rectangle((96 * k, 156 * k, 150 * k, 168 * k), 6 * k, fill="#1B1E2B")
d.rounded_rectangle((96 * k, 222 * k, 140 * k, 238 * k), 8 * k, fill="#F95B1C")
cx, cy, r = 236, 226, 46
pts = [(cx, cy - r), (cx + 11, cy - 11), (cx + r, cy), (cx + 11, cy + 11), (cx, cy + r), (cx - 11, cy + 11), (cx - r, cy), (cx - 11, cy - 11)]
d.polygon([(x * k, y * k) for x, y in pts], fill="#FFC53D")
im.resize((S, S), Image.LANCZOS).save(OUT / "agent.png")
print("ok", sorted(p.name for p in OUT.iterdir()))
