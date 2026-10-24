"""Design House post şablonları (1080×1350). Instagram dili İngilizce."""
from engine import doc, asset
MONO = asset("design-house/logo-tile.png")
SITE, TEL = "designhouseglobal.com", "0212 287 86 06"

CSS = """
:root{--k:#0B0B0B;--cr:#F4F1EA;--w:#902825;--g:#D49C49;--li:#D8F24A;--co:#EC6242;--la:#C9C2F0;--ic:#A9D6E5;--bu:#F0E2A6}
.post{font-family:Archivo;color:var(--cr);background:var(--k)}
.cream{background:var(--cr);color:var(--k)}
.wine{background:radial-gradient(120% 80% at 70% 20%,#3a0f12 0%,#140405 55%,#0B0B0B 100%)}
.deco{position:absolute;pointer-events:none}
.mono{position:absolute;left:56px;top:56px;width:118px;border-radius:14px}
.lab{font:500 22px/1 'DM Mono';letter-spacing:.14em;text-transform:uppercase;opacity:.8}
.top{position:absolute;left:64px;top:210px}
.osw{font-family:Oswald;font-weight:600;text-transform:uppercase;line-height:.98;letter-spacing:-.005em}
.blk{font-family:Archivo;font-weight:900;text-transform:uppercase;letter-spacing:-.035em;line-height:.92}
.bold{font-family:Archivo;font-weight:700;text-transform:uppercase;letter-spacing:-.01em;line-height:1.05}
.gold{color:var(--g)}
.foot{position:absolute;left:0;right:0;bottom:0;height:88px;display:flex;align-items:center;justify-content:center;gap:26px;font:500 21px/1 'DM Mono';letter-spacing:.14em;text-transform:uppercase}
.foot::before,.foot::after{content:"";flex:1;height:1px;background:currentColor;opacity:.4;margin:0 40px}
.cta{display:inline-block;background:var(--g);color:var(--k);padding:22px 34px;border-radius:8px;font:700 27px/1 Archivo}
.dots{position:absolute;bottom:112px;left:0;right:0;display:flex;justify-content:center;gap:10px}.dots i{width:10px;height:10px;border-radius:50%;background:rgba(244,241,234,.3)}.dots i.on{background:var(--g)}
.arrow{font:500 26px/1 'DM Mono';letter-spacing:.1em;text-transform:uppercase}
"""
def mono(): return f'<img class="mono" src="{MONO}">'
def foot(dark=True): return f'<div class="foot" style="color:{"#F4F1EA" if dark else "#0B0B0B"}"><span>{SITE}</span><span>|</span><span>{TEL}</span></div>'
def dots(n, i): return '<div class="dots">' + "".join(f'<i class="{"on" if k==i else ""}"></i>' for k in range(n)) + "</div>"
def post(inner, cls=""): return doc(CSS, f'<div class="post {cls}">{inner}</div>', lang="en")

def sheets():
    r = ""
    for k, (x, y, rot) in enumerate([(560, 100, -4), (790, 120, 3), (575, 380, 2), (800, 400, -3)]):
        r += f'<div class="deco" style="left:{x}px;top:{y}px;width:200px;height:250px;border:3px solid #D49C49;border-radius:6px;transform:rotate({rot}deg);background:rgba(212,156,73,.06)"><div style="position:absolute;left:14px;bottom:12px;font:500 20px/1 \'DM Mono\';color:#D49C49">0{k+1}</div><div style="position:absolute;left:24px;right:24px;top:30px;height:120px;border:2px dashed rgba(212,156,73,.6)"></div><div style="position:absolute;left:50%;top:-12px;width:18px;height:18px;border-radius:50%;background:#902825;transform:translateX(-50%)"></div></div>'
    return r

def lesson(d):
    return post(f'''{sheets()}{mono()}
    <div style="position:absolute;left:64px;right:64px;top:640px">
      <div class="lab gold" style="margin-bottom:26px">{d["lab"]}</div>
      <div class="osw" style="font-size:132px">{d["h1"]}</div>
      <div class="osw gold" style="font-size:86px;margin-top:6px">{d["h2"]}</div>
      <div style="width:120px;height:3px;background:var(--g);margin:28px 0"></div>
      <p style="font:500 30px/1.4 Archivo;max-width:860px">{d["body"]} <span class="gold">{d["rule"]}</span></p>
      <div style="margin-top:34px"><span class="cta">{d["cta"]}</span></div>
    </div>{foot()}''', "wine")

def statement(d):
    return post(f'''{mono()}<div class="deco blk" style="right:-40px;top:120px;font-size:620px;color:rgba(144,40,37,.18)">—</div>
    <div class="top"><div class="lab">{d["lab"]}</div></div>
    <div style="position:absolute;left:64px;right:64px;bottom:250px">
      <div class="bold" style="font-size:96px">{d["l1"]}&nbsp;—<br><span class="gold">{d["l2"]}</span></div>
      <p style="font:500 34px/1.4 Archivo;margin-top:36px;max-width:780px;opacity:.9">{d["sub"]}</p>
    </div>{foot()}''', "wine")

def dest_cover(d):
    return post(f'''{mono()}<div class="deco blk" style="left:-30px;top:200px;font-size:300px;color:transparent;-webkit-text-stroke:2px rgba(212,156,73,.13);line-height:.9">{d["bg"]}</div>
    <div style="position:absolute;left:64px;right:64px;bottom:250px">
      <div class="lab" style="margin-bottom:24px">Design House — student destinations</div>
      <div class="osw" style="font-size:170px">{d["h"]}</div>
      <div class="osw" style="font-size:40px;margin-top:28px;font-weight:400;letter-spacing:.02em">{d["sub"]}</div>
    </div>{dots(d["n"],0)}{foot()}''', "wine")

def dest_city(d):
    return post(f'''{mono()}<div class="deco blk" style="left:-20px;top:170px;font-size:{d.get("bgsize",250)}px;color:transparent;-webkit-text-stroke:2px rgba(244,241,234,.16)">{d["city"]}</div>
    <div class="deco" style="right:64px;top:70px" ><span class="lab">( 0{d["i"]} / {d["city"]} )</span></div>
    <div style="position:absolute;left:64px;right:64px;bottom:250px">
      <div class="lab gold" style="margin-bottom:24px">{d["where"]}</div>
      <div class="osw" style="font-size:150px">{d["schools"]}</div>
      <div style="font:500 32px/1.35 Archivo;margin-top:28px;text-transform:uppercase;letter-spacing:.01em;max-width:860px">{d["line"]}</div>
      {('<div style="font:700 30px/1 Archivo;margin-top:22px;text-transform:uppercase" class="gold">'+d["end"]+'</div>') if d.get("end") else ""}
    </div>{dots(d["n"],d["i"])}{foot()}''', "wine")

def paths(d):
    cards = "".join(f'<div style="background:{c};border-radius:6px;padding:24px 24px;height:300px;display:flex;flex-direction:column;justify-content:space-between;color:#0B0B0B"><div style="display:flex;justify-content:space-between;font:500 18px/1 \'DM Mono\';letter-spacing:.1em;text-transform:uppercase"><b style="font:900 28px/1 Archivo">0{k+1}</b><span>{s}</span></div><div class="blk" style="font-size:50px;line-height:.95">{t}</div></div>' for k, (t, s, c) in enumerate(d["paths"]))
    return post(f'''<div class="deco" style="left:64px;top:64px"><span class="blk" style="font-size:34px;letter-spacing:-.02em;color:#0B0B0B">DESIGN HOUSE<span style="color:#D8F24A;-webkit-text-stroke:1px #0B0B0B">.</span></span></div>
    <div class="deco" style="right:64px;top:72px"><span class="lab" style="color:#0B0B0B">( Disciplines ) 02</span></div>
    <div style="position:absolute;left:64px;right:64px;top:170px">
      <div class="blk" style="font-size:130px;color:#0B0B0B">{d.get("h", "Six creative<br>paths.")}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin:46px 0 36px">{cards}</div>
      <div class="arrow" style="color:#0B0B0B">{d.get("cta","Find your path -&gt;")}</div>
    </div>{foot(False)}''', "cream")

def numbers(d):
    rows = "".join(f'<div style="display:flex;align-items:baseline;gap:24px;padding:34px 0;border-bottom:2px solid #0B0B0B"><span class="blk" style="font-size:150px;color:#0B0B0B">{a}</span><span class="lab" style="color:#0B0B0B;opacity:1">{b}</span></div>' for a, b in d["rows"])
    return post(f'''<div class="deco" style="left:0;right:0;top:0;height:150px;background:#C9C2F0"></div>
    <div class="deco" style="left:64px;top:56px"><span class="blk" style="font-size:34px;color:#0B0B0B">DESIGN HOUSE<span style="color:#D8F24A;-webkit-text-stroke:1px #0B0B0B">.</span></span></div>
    <div class="deco" style="right:64px;top:64px"><span class="lab" style="color:#0B0B0B">( By the numbers ) 05</span></div>
    <div style="position:absolute;left:64px;right:64px;top:200px">{rows}
      <p style="font:500 30px/1.4 Archivo;color:#0B0B0B;margin-top:36px">{d["end"]} <i style="color:#EC6242">{d["it"]}</i></p></div>{foot(False)}''', "cream")

def future(d):
    return post(f'''<div class="deco" style="left:64px;top:64px"><span class="blk" style="font-size:34px">DESIGN HOUSE<span style="color:#D8F24A">.</span></span></div>
    <div class="deco" style="right:64px;top:72px"><span class="lab">( New business ) 06</span></div>
    <div style="position:absolute;left:64px;right:64px;top:330px">
      <div class="blk" style="font-size:200px">Build<br>your<br>future<span style="color:#D8F24A">.</span></div>
      <p style="font:500 36px/1.4 Archivo;margin:44px 0 40px;max-width:800px">{d["body"]}</p>
      <div class="arrow" style="color:#D8F24A">{d["cta"]} -&gt;</div>
    </div>{foot()}''')

def library():
    n = 4
    return [
      ("01-portfolio-lesson", lesson(dict(lab="( Portfolio lesson 05 )", h1="Show the turn.", h2="Not just the end.",
        body="Reviewers want to see where your idea changed direction, and why.", rule="2–3 pages that show a pivot, labeled by date.", cta="Explore your creative direction."))),
      ("02-statement", statement(dict(lab="( Studio notes )", l1="Your first idea", l2="is rarely your best one.", sub="Keep it. Then make three more. The fourth one usually knows what it wants to be."))),
      ("03-destinations-1-kapak", dest_cover(dict(n=n, bg="LONDON<br>NEW YORK<br>MILAN", h="Where our<br>students<br>get in.", sub="Three cities. Six schools. One studio."))),
      ("03-destinations-2", dest_city(dict(n=n, i=1, city="London", where="London", schools="Central Saint<br>Martins + RCA.", line="Where a portfolio is read like a point of view."))),
      ("03-destinations-3", dest_city(dict(n=n, i=2, city="New York", bgsize=200, where="New York", schools="Parsons<br>+ Pratt.", line="Two schools where making is a way of thinking."))),
      ("03-destinations-4", dest_city(dict(n=n, i=3, city="Milan", where="Milan", schools="Politecnico<br>+ NABA.", line="Design culture with a technical spine.", end="Build your application with Design House."))),
      ("04-six-paths", paths(dict(paths=[("Spatial<br>design", "Architecture", "#A9D6E5"), ("Visual<br>comms", "Graphic & type", "#EC6242"), ("Fine<br>arts", "Studio practice", "#F0E2A6"),
        ("Indus-<br>trial", "Product & object", "#D8F24A"), ("Fashion", "Concept & textile", "#C9C2F0"), ("Photo<br>& film", "Storytelling", "#A9D6E5")]))),
      ("05-by-the-numbers", numbers(dict(rows=[("12+", "Years"), ("900+", "Students"), ("40+", "Schools"), ("96%", "Accepted")], end="Twelve years of portfolios,", it="zero boring ones."))),
      ("06-build-your-future", future(dict(body="Portfolio prep, mentorship and admissions strategy for the world's best art & design schools.", cta="DM “REVIEW” to book a portfolio review"))),
    ]

META = dict(
  brand="design_house", lang="en",
  intro="Six series joining the two identities: wine and gold for portfolio lessons and destinations, the website's cream, black and pastels for studio and numbers. One headline, one lesson, one rule per post.",
  constants=["One logo per post: DG monogram on wine posts, “DESIGN HOUSE.” wordmark on cream posts", "Gold only on a single line or CTA", "Oswald-type condensed headlines on Instagram, Archivo 900 for web-style posts", "DM Mono for labels: ( Label ) 02"],
  series=[
    dict(id="01", name="Portfolio Lesson", img=["01-portfolio-lesson"], when="One concrete portfolio rule, explained like a tutor.", freq="Weekly", fmt="Single · wine & gold",
      slots=["Pinned process sheets 01–04", "DM Mono lesson number", "Condensed headline + gold second line", "One rule in gold + gold CTA"],
      caption="Most applicants show the final piece and hide the turn that made it.\n\nReviewers read for thinking. Show 2–3 pages where your idea changed direction, labeled by date.\n\nDM WORKSHOP — global cohort.\n#DesignHouseGlobal #PortfolioPreparation #ArtAndDesignEducation"),
    dict(id="02", name="Studio Notes", img=["02-statement"], when="A short “X — Y.” idea that sticks.", freq="Weekly", fmt="Single · wine",
      slots=["DM Mono label", "Bold statement: line 1 cream, line 2 gold", "One-sentence follow-up"],
      caption="Your first idea — is rarely your best one.\n\nKeep it. Then make three more. The fourth one usually knows what it wants to be.\n#DesignHouseGlobal #CreativeProcess #PortfolioPreparation"),
    dict(id="03", name="Destinations", img=["03-destinations-1-kapak", "03-destinations-2", "03-destinations-3", "03-destinations-4"], when="Showing where students get in, city by city.", freq="Monthly", fmt="Carousel · 4 slides",
      slots=["Cover: city names as outline texture", "One city per slide: ( 0X / CITY ) label", "Schools in condensed caps", "One original line per city; gold closing CTA"],
      caption="Where our students get in. 🌍\n\nLondon, New York, Milan: three cities, six schools, one studio shaping your next chapter.\n\nBuild your portfolio. Find your direction.\n#DesignHouseGlobal #CentralSaintMartins #Parsons #Pratt #NABA"),
    dict(id="04", name="Six Paths", img=["04-six-paths"], when="Bringing the website's discipline cards to Instagram.", freq="Monthly", fmt="Single · cream",
      slots=["Wordmark + ( Disciplines ) label", "Archivo 900 headline", "Six pastel cards, colours as on the website", "Mono arrow link"],
      caption="Six creative paths. One studio.\n\nSpatial design, visual comms, fine arts, industrial, fashion, photo & film. Which one fits how you think?\n#DesignHouseGlobal #ArtAndDesign #CreativePortfolio"),
    dict(id="05", name="By the Numbers", img=["05-by-the-numbers"], when="Proof from the website, in its own style.", freq="Quarterly", fmt="Single · cream & lavender",
      slots=["Lavender band like the website", "Four numbers with mono labels", "Witty closing line, italic in coral"],
      caption="12+ years. 900+ students. 40+ schools. 96% accepted.\n\nTwelve years of portfolios, zero boring ones.\n#DesignHouseGlobal #PortfolioPreparation"),
    dict(id="06", name="Build Your Future", img=["06-build-your-future"], when="The consultation call to action.", freq="Monthly · before deadlines", fmt="Single · black",
      slots=["Wordmark + ( New business ) label", "Huge Archivo headline with lime full stop", "One-line offer", "Lime mono DM call to action"],
      caption="Build your future.\n\nPortfolio prep, mentorship and admissions strategy for the world's best art & design schools.\n\nDM “REVIEW” to book a portfolio review.\n#DesignHouseGlobal #PortfolioReview"),
  ],
  calendar=[("Mon","Portfolio Lesson","Show the turn"),("Tue","Studio Notes","First idea"),("Wed","Destinations","London · NY · Milan"),("Thu","Video","Studio day"),("Fri","Six Paths","Disciplines"),
            ("Mon","Portfolio Lesson","Open with a decision"),("Tue","Studio Notes","Consistency"),("Wed","By the Numbers","Proof"),("Thu","Video","InArts fair"),("Fri","Build Your Future","Book a review")],
  hooks=["… — is not …", "Open with a decision, not a decoration.", "Most applicants … Reviewers …", "Where our students get in.", "Six schools. Three cities. One studio.", "Show the turn.", "The brief — is only the beginning.", "Your portfolio — is not your archive.", "Good ideas — don't grow alone.", "Places are limited."],
  ctas=["Explore your creative direction.", "DM “REVIEW” to book a portfolio review", "Find your path ->", "DM WORKSHOP — global cohort.", "Build your application with Design House."],
)


# ---------- Instagram Story (1080×1920) ----------
def story(d):
    """Story: şarap zemin, dar krem başlık + altın son satır, altın CTA. d: tag, title[list], body, cta"""
    lines = d["title"]; n = len(lines)
    t = "".join(f'<span class="gold" style="display:block;white-space:nowrap">{x}</span>' if k == n - 1 else f'<span style="display:block;white-space:nowrap">{x}</span>' for k, x in enumerate(lines))
    return doc(CSS, f'''<div class="post wine"><div class="deco blk" style="right:-60px;top:330px;font-size:760px;color:rgba(144,40,37,.16)">—</div>
    <img class="mono" src="{MONO}" style="top:220px">
    <div style="position:absolute;left:72px;right:72px;top:380px;bottom:300px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start">
      <div class="lab gold" style="margin-bottom:34px">{d["tag"]}</div>
      <div class="osw" style="font-size:118px">{t}</div>
      <div style="width:140px;height:3px;background:var(--g);margin:44px 0"></div>
      <p style="font:500 38px/1.42 Archivo;max-width:900px;opacity:.92">{d["body"]}</p>
      <div style="margin-top:56px"><span class="cta" style="font-size:30px;padding:26px 40px">{d["cta"]}</span></div>
    </div>
    <div class="foot" style="color:#F4F1EA;height:110px"><span>{SITE}</span><span>|</span><span>{TEL}</span></div></div>''', lang="en", h=1920)


# ---------- Görünüm temaları (Brand Kit paleti içinde zemin seçenekleri) ----------
NO_THEME = {"paths", "numbers", "service"}   # kendi sabit zemini olan şablonlar
THEMES = {
  "sarap": {"name": "Şarap rengi", "css": """
.post.th-sarap{background:radial-gradient(120% 80% at 70% 20%,#3a0f12 0%,#140405 55%,#0B0B0B 100%)!important;color:var(--cr)!important}"""},
  "siyah": {"name": "Siyah (web sitesi kapanışı gibi)", "css": """
.post.th-siyah{background:var(--k)!important;color:var(--cr)!important}"""},
  "krem": {"name": "Krem (web sitesi gibi)", "css": """
.post.th-krem{background:var(--cr)!important;color:var(--k)!important}
.th-krem .gold,.th-krem .arrow{color:var(--w)!important}
.th-krem .foot{color:var(--k)!important}
.th-krem .deco.blk{-webkit-text-stroke-color:rgba(11,11,11,.10)!important}
.th-krem [style*="background:var(--g)"]{background:var(--w)!important}
.th-krem .cta{background:var(--w)!important;color:var(--cr)!important}
.th-krem .dots i{background:rgba(11,11,11,.25)}.th-krem .dots i.on{background:var(--w)}"""},
}


# ---------- Yeni kompozisyon aileleri ----------
PHOTO_SLOT = {"service", "badge"}

def service(d):
    """Seri: Servis Bloğu — web sitesindeki bölünmüş blok: solda görsel panel, sağda mercan rakam, Archivo başlık, metin, ok.
    d: idx, lab, title, body, cta, photo(isteğe bağlı)"""
    panel = (f'<img src="{d["photo"]}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">' if d.get("photo") else
             f'<div style="position:absolute;inset:0;background:radial-gradient(120% 90% at 30% 20%,#3a0f12,#140405 60%,#0B0B0B)"></div>'
             f'<div class="deco" style="left:70px;top:90px;width:300px;height:380px;border:3px solid #D49C49;border-radius:6px;transform:rotate(-5deg)"></div>'
             f'<div class="deco" style="left:120px;top:300px;width:280px;height:360px;border:3px solid rgba(212,156,73,.6);border-radius:6px;transform:rotate(4deg);background:rgba(144,40,37,.25)"></div>'
             f'<div class="deco blk" style="left:40px;bottom:40px;font-size:240px;color:transparent;-webkit-text-stroke:2px rgba(212,156,73,.45)">{d["idx"]}</div>')
    return post(f'''<div class="deco" style="left:64px;top:64px"><span class="blk" style="font-size:34px;color:#0B0B0B">DESIGN HOUSE<span style="color:#D8F24A;-webkit-text-stroke:1px #0B0B0B">.</span></span></div>
    <div class="deco" style="right:64px;top:72px"><span class="lab" style="color:#0B0B0B">{d["lab"]}</span></div>
    <div style="position:absolute;left:0;top:170px;width:470px;bottom:120px;overflow:hidden">{panel}</div>
    <div style="position:absolute;left:530px;right:64px;top:250px;color:#0B0B0B">
      <div class="blk" style="font-size:150px;color:#EC6242">{d["idx"]}</div>
      <div class="blk" style="font-size:66px;line-height:.98;margin-top:34px">{d["title"]}</div>
      <p style="font:500 30px/1.45 Archivo;margin:34px 0 40px">{d["body"]}</p>
      <div class="arrow">{d["cta"]} -&gt;</div>
    </div>{foot(False)}''', "cream")

def badge(d):
    """Seri: Rozetli Ders — üstte kicker ve dev dar başlık, sağda altın rozet (somut kural), altta kısa açıklama.
    d: kicker, h1, h2, h3, rule, body, photo(isteğe bağlı)"""
    vis = (f'<img class="photo" src="{d["photo"]}" style="opacity:.35">' if d.get("photo") else
           '<div class="deco blk" style="left:-40px;bottom:120px;font-size:540px;color:rgba(144,40,37,.16);line-height:.8">“</div>')
    return post(f'''{vis}{mono()}
    <div style="position:absolute;left:64px;right:64px;top:230px">
      <div class="lab gold" style="max-width:640px;line-height:1.5">{d["kicker"]}</div>
      <div class="osw" style="font-size:118px;margin-top:30px;white-space:nowrap">{d["h1"]}<br>{d["h2"]}<br><span class="gold">{d["h3"]}</span></div></div>
    <div style="position:absolute;right:70px;top:800px;width:270px;height:270px;border-radius:50%;background:var(--g);color:#0B0B0B;display:grid;place-items:center;text-align:center;padding:40px;transform:rotate(-8deg);font:700 30px/1.15 Archivo;text-transform:uppercase">{d["rule"]}</div>
    <p style="position:absolute;left:64px;width:580px;top:840px;font:500 31px/1.42 Archivo;opacity:.92">{d["body"]}</p>
    {foot()}''', "wine")


# ---------- Kütüphane: yeni kompozisyon aileleri ve Story ----------
_LIB0 = library
def library():
    return _LIB0() + [
      ("07-service-block", service(dict(idx="01", lab="( What we do ) 01", title="Portfolio<br>direction.",
        body="We help you find the thread that connects your projects, then edit until every page earns its place.", cta="Book a portfolio review"))),
      ("08-badge-lesson", badge(dict(kicker="Nobody asks what software you used for the cover.", h1="Open with", h2="a decision,", h3="not decoration.",
        rule="15–20 words.<br>One cover.", body="The first page tells the reviewer how you think. Make it a choice, not a collage."))),
      ("09-story", story(dict(tag="( Studio notes )", title=["Your first idea —", "is rarely", "your best one."],
        body="Keep it. Then make three more. The fourth one usually knows what it wants to be.", cta="DM “REVIEW”"))),
    ]

META["intro"] = ("Eight feed series and one Story layout, built from both sides of the brand: the wine-and-gold Instagram studio look and the "
                 "cream, Archivo-heavy website. Composition families: lesson with pinned sheets, X — Y statement, city carousel, pastel discipline "
                 "grid, number band, black CTA, website split block and a badge lesson.")
META["series"] += [
  dict(id="07", name="Service Block", img=["07-service-block"], when="Explaining one service (portfolio, mentorship, admissions) in the website's split-block language.",
       freq="Monthly", fmt="Single · cream split",
       slots=["Wordmark + ( What we do ) label", "Left panel: uploaded photo or wine panel with sheets", "Coral index number + Archivo headline", "Body + mono arrow link"],
       caption="Portfolio direction. ✏️\n\nWe find the thread that connects your projects, then edit until every page earns its place.\n\nDM “REVIEW” to book a portfolio review.\n#DesignHouseGlobal #PortfolioReview #ArtAndDesign"),
  dict(id="08", name="Badge Lesson", img=["08-badge-lesson"], when="One sharp portfolio rule with a memorable number or limit on a gold badge.",
       freq="Every 2 weeks", fmt="Single · wine + badge",
       slots=["Gold mono kicker", "Three-line condensed headline, last line gold", "Rotated gold badge with the rule", "One-sentence explanation"],
       caption="Open with a decision, not decoration. 🎯\n\nNobody asks what software you used for the cover. They ask what you decided. 15–20 words. One cover.\n#DesignHouseGlobal #PortfolioTips #ArtSchool"),
  dict(id="09", name="Instagram Story", img=["09-story"], when="A one-screen studio note supporting a feed post; 1080×1920.",
       freq="With feed posts", fmt="Story · 9:16",
       slots=["Safe zones top and bottom", "Mono label in gold", "Condensed cream headline, last line gold", "Gold CTA"],
       caption="Stories have no caption; highlight note: “Studio notes.” #DesignHouseGlobal"),
]
