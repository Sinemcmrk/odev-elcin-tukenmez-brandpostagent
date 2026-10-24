"""Post şablon motoru: HTML/CSS şablonlarını PNG'ye çevirir (Feed 1080×1350, Story 1080×1920).

- doc(css, body): şablonun HTML belgesini kurar (fontlar dahil).
- asset(yol): assets/ klasöründeki bir dosyanın tarayıcı yolunu verir.
- with_photo(html, foto, opaklik): herhangi bir şablona tam sayfa fotoğraf katmanı ekler.
- render([(ad, html), ...], cikis_klasoru): PNG üretir, taşan metni uyarı olarak yazar.
"""
import asyncio, os, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent
F = (ROOT / "fonts").as_uri()

def asset(rel):
    """assets/ altındaki dosya için file:// yolu."""
    return (ROOT / "assets" / rel).as_uri()

def _src(p):
    """Fotoğraf için yerel yol ya da http(s)/file adresi kabul eder."""
    if p.startswith(("http://", "https://", "file://", "data:")): return p
    return pathlib.Path(p).resolve().as_uri()

FONTS = f"""
@font-face{{font-family:'Montserrat';src:url('{F}/Montserrat.ttf');font-weight:100 900}}
@font-face{{font-family:'Playfair Display';src:url('{F}/PlayfairDisplay.ttf');font-weight:400 900}}
@font-face{{font-family:'Oswald';src:url('{F}/Oswald.ttf');font-weight:200 700}}
@font-face{{font-family:'Roboto';src:url('{F}/Roboto.ttf');font-weight:100 900}}
@font-face{{font-family:'Archivo';src:url('{F}/Archivo.ttf');font-weight:100 900;font-stretch:62% 125%}}
@font-face{{font-family:'Archivo Black';src:url('{F}/ArchivoBlack-Regular.ttf')}}
@font-face{{font-family:'DM Mono';src:url('{F}/DMMono-Regular.ttf');font-weight:400}}
@font-face{{font-family:'DM Mono';src:url('{F}/DMMono-Medium.ttf');font-weight:500}}
@font-face{{font-family:'Poppins';src:url('{F}/Poppins-Regular.ttf');font-weight:400}}
@font-face{{font-family:'Poppins';src:url('{F}/Poppins-SemiBold.ttf');font-weight:600}}
@font-face{{font-family:'Poppins';src:url('{F}/Poppins-Bold.ttf');font-weight:700}}
@font-face{{font-family:'Poppins';src:url('{F}/Poppins-ExtraBold.ttf');font-weight:800}}
@font-face{{font-family:'Poppins';font-style:italic;src:url('{F}/Poppins-LightItalic.ttf');font-weight:300}}
"""
BASE = ("*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:HHpx;overflow:hidden}"
        ".post{width:1080px;height:HHpx;position:relative;overflow:hidden}"
        ".photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none}")

def doc(css, body, lang="tr", h=1350):
    """h: 1350 = Instagram Feed (4:5), 1920 = Instagram Story (9:16)."""
    base = BASE.replace("HH", str(h))
    return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>{FONTS}{base}{css}</style></head><body data-h="{h}">{body}</body></html>'

def with_photo(html, photo, opacity=0.3, blend="luminosity"):
    """Şablonun arka planına fotoğraf ekler; metinler fotoğrafın üstünde kalır."""
    i = html.index('<div class="post'); j = html.index(">", i) + 1
    img = f'<img class="photo" src="{_src(photo)}" style="opacity:{opacity};mix-blend-mode:{blend}">'
    return html[:j] + img + html[j:]

def _height(html):
    m = re.search(r'data-h="(\d+)"', html)
    return int(m.group(1)) if m else 1350

def with_theme(html, theme, themes):
    """Markanın tanımlı görünüm temalarından birini (zemin + metin renkleri) şablona uygular.
    Tema yalnızca Brand Kit paletindeki renkleri kullanır; logo, font ve iletişim bandı değişmez."""
    if not theme or theme not in themes:
        return html
    html = html.replace('<div class="post', f'<div class="post th-{theme}', 1)
    return html.replace("</style>", themes[theme]["css"] + "</style>", 1)

async def _render(items, outdir, shots=True):
    from playwright.async_api import async_playwright
    os.makedirs(outdir, exist_ok=True)
    report = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for name, html in items:
            hp = os.path.join(outdir, name + ".html")
            open(hp, "w", encoding="utf-8").write(html)
            await pg.set_viewport_size({"width": 1080, "height": _height(html)})
            await pg.goto(pathlib.Path(hp).resolve().as_uri())
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(150)
            ov = await pg.evaluate("""()=>{const o=[];const P=document.querySelector('.post').getBoundingClientRect();
              const f=document.querySelector('.post .foot');const d=document.querySelector('.post .dots');
              let lim=P.bottom; if(f) lim=Math.min(lim,f.getBoundingClientRect().top); if(d) lim=Math.min(lim,d.getBoundingClientRect().top-4);
              const skip=e=>e.closest('.deco,.foot,.dots,.photo,.tile,.logo,.mono,.art,.page');
              document.querySelectorAll('.post *').forEach(e=>{if(skip(e))return;const hasText=[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim());if(!hasText)return;
                const r=e.getBoundingClientRect();if(!r.width)return;
                if(r.right>P.right+1||r.left<P.left-1||r.bottom>lim+2||e.scrollWidth>e.clientWidth+3&&getComputedStyle(e).display!='inline')o.push((e.innerText||'').trim().slice(0,40))});
              return [...new Set(o)]}""")
            report[name] = ov
            if ov: print("  ! taşma:", name, ov[:3])
            if shots:
                await pg.screenshot(path=os.path.join(outdir, name + ".png"))
            os.remove(hp)
        await b.close()
    return report

def render(items, outdir, shots=True):
    """PNG üretir; {post_adı: [alana sığmayan metinler]} döndürür.
    shots=False: yalnızca yerleşimi ölçer, PNG yazmaz (Agent 1'in sığma kontrolü)."""
    return asyncio.run(_render(items, outdir, shots))
