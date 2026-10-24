"""Education for Innovation (E4I) post şablonları (1080×1350). Instagram dili İngilizce."""
from engine import doc, asset
LOGO = asset("e4i/logo.png")   # Instagram'daki gibi: kutusuz logo, yeşil yazı
SITE, TEL = "educationforinnovation.org", "+90 212 287 8606"   # Instagram'daki numara

CSS = """
:root{--n:#050E1F;--n2:#111C3A;--g:#18B77D;--gf:#17A26B;--p:#7847D6;--o:#FF671B;--l:#B0FE25;--cr:#FFF1D4}
.post{font-family:Roboto;color:#fff;background:var(--n)}
.deco{position:absolute;pointer-events:none}
.logo{position:absolute;right:56px;top:60px;width:230px}
.pill{display:inline-block;padding:14px 26px;border-radius:99px;background:var(--cr);color:var(--n);font:800 22px/1 Roboto;letter-spacing:.06em;text-transform:uppercase}
.pill.p{background:var(--p);color:#fff}.pill.l{background:var(--l);color:var(--n)}
.top{position:absolute;left:64px;top:72px}
.H{font-family:'Archivo Black';text-transform:uppercase;line-height:1.02;letter-spacing:-.005em}
.H .o{color:var(--o)}.H .l{color:var(--l)}
.foot{position:absolute;left:0;right:0;bottom:0;height:90px;background:var(--gf);color:var(--n);display:flex;justify-content:center;align-items:center;gap:30px;font:700 24px/1 Roboto}
.bar{display:flex;align-items:center;justify-content:center;height:72px;border-radius:12px;font:400 28px/1 'Archivo Black';text-transform:uppercase;letter-spacing:.02em}
.bar.g{background:var(--g)}.bar.p{background:var(--p)}.bar.o{background:var(--o)}
.card{border-radius:30px;background:rgba(17,28,58,.92);box-shadow:inset 0 0 0 2px rgba(255,255,255,.12);padding:46px 44px}
.row{display:flex;align-items:center;gap:24px;border-radius:20px;padding:24px 28px;box-shadow:inset 0 0 0 3px var(--c);font:400 30px/1.15 'Archivo Black';text-transform:uppercase}
.row i{flex:none;width:58px;height:58px;border-radius:50%;background:var(--c);display:grid;place-items:center;font:900 28px/1 Roboto;font-style:normal}
.cta{display:inline-block;padding:22px 40px;border-radius:14px;box-shadow:inset 0 0 0 3px var(--l);font:400 24px/1 'Archivo Black';text-transform:uppercase;color:#fff}
.cta.cr{background:var(--cr);color:var(--n);box-shadow:none;border-radius:20px}
.lime{font:400 30px/1 'Archivo Black';color:var(--l);text-transform:uppercase}
.dots{position:absolute;bottom:118px;left:0;right:0;display:flex;justify-content:center;gap:12px}.dots i{width:12px;height:12px;border-radius:50%;background:rgba(255,255,255,.3)}.dots i.on{background:var(--l);width:34px;border-radius:6px}
.glow{position:absolute;border-radius:50%;filter:blur(100px)}
.art{position:absolute;left:0;right:0;top:0;height:470px;overflow:hidden;background:linear-gradient(135deg,#1A1145 0%,#0B1A3A 55%,#2A1408 100%)}
"""

def rings(x, y, s=1.0, op=.9):
    cs = [("#774A9D", 200), ("#E01E26", 150), ("#F28123", 100)]
    c = "".join(f'<circle cx="230" cy="230" r="{r}" fill="none" stroke="{col}" stroke-width="10"/>' for col, r in cs)
    return f'<svg class="deco" style="left:{x}px;top:{y}px;opacity:{op}" width="{460*s:.0f}" height="{460*s:.0f}" viewBox="0 0 460 460">{c}</svg>'

def spark(x, y, sz=40, c="#B0FE25"): return f'<div class="deco" style="left:{x}px;top:{y}px;font-size:{sz}px;color:{c}">✦</div>'
def glow(x, y, d, c, op=.5): return f'<div class="deco glow" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;background:{c};opacity:{op}"></div>'
def grid():
    l = "".join(f'<line x1="{i*90}" y1="0" x2="{i*90}" y2="470" stroke="rgba(176,254,37,.12)"/>' for i in range(13))
    l += "".join(f'<line x1="0" y1="{i*90}" x2="1080" y2="{i*90}" stroke="rgba(176,254,37,.12)"/>' for i in range(6))
    return f'<svg class="deco" style="left:0;top:0" width="1080" height="470">{l}</svg>'
def logo(): return f'<img class="logo" src="{LOGO}">'
def foot(): return f'<div class="foot"><span>{SITE}</span><span style="opacity:.5">•</span><span>{TEL}</span></div>'
def dots(n, i): return '<div class="dots">' + "".join(f'<i class="{"on" if k==i else ""}"></i>' for k in range(n)) + "</div>"
def post(inner): return doc(CSS, f'<div class="post">{inner}</div>', lang="en")

def art(extra=""):
    return f'<div class="art">{grid()}{glow(120,40,420,"#7847D6",.55)}{glow(640,120,380,"#FF671B",.45)}{rings(560,20,0.95,.8)}{spark(140,120,46)}{spark(420,300,30,"#FFF1D4")}{spark(900,380,34)}{extra}</div>'

def program(d):
    bars = "".join(f'<div class="bar {c}" style="justify-content:flex-start;padding:0 28px;gap:16px"><span style="opacity:.8">{k}</span>•<span>{v}</span></div>' for c, k, v in d["bars"])
    return post(f'''{art()}{logo()}
    <div class="top" style="top:400px"><span class="pill p">{d["tag"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;top:480px">
      <div class="H" style="font-size:96px">{d["h"]}</div>
      <div style="display:grid;gap:14px;margin:40px 0 40px">{bars}</div>
      <span class="cta">{d["cta"]}</span>
    </div>{foot()}''')

def play_cover(d):
    return post(f'''{art()}{logo()}
    <div class="top" style="top:400px"><span class="pill">{d["tag"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;top:490px">
      <div class="H" style="font-size:100px">{d["h"]}</div>
      <div style="display:flex;gap:14px;margin:40px 0 34px">{"".join(f'<div class="bar {c}" style="flex:1">{t}</div>' for c, t in zip("gpo", d["steps"]))}</div>
      <span class="cta cr">{d.get("cta","Save this playbook")}</span>
    </div>{dots(d["n"],0)}{foot()}''')

def play_step(d):
    cols = ["#18B77D", "#7847D6", "#FF671B"]
    rows = "".join(f'<div class="row" style="--c:{cols[k]}"><i>{k+1}</i><span>{x}</span></div>' for k, x in enumerate(d["rows"]))
    return post(f'''{art()}{logo()}
    <div class="top"><span class="pill">STEP 0{d["i"]} • {d["step"]}</span></div>
    <div style="position:absolute;left:44px;right:44px;top:380px" class="card">
      <div class="H" style="font-size:88px">{d["h1"]}<br><span class="o">{d["h2"]}</span></div>
      <div style="display:grid;gap:18px;margin:34px 0 34px">{rows}</div>
      <div style="text-align:center">{('<span class="cta cr">'+d["end"]+'</span>') if d.get("btn") else ('<span class="lime">'+d["end"]+'</span>')}</div>
    </div>{dots(d["n"],d["i"])}{foot()}''')

def field(d):
    bars = "".join(f'<div class="bar {c}" style="justify-content:flex-start;padding:0 28px;gap:16px;font-size:26px"><span style="opacity:.8">{k}</span>•<span>{v}</span></div>' for c, k, v in d["bars"])
    return post(f'''{glow(-200,-100,620,"#7847D6",.45)}{glow(600,700,560,"#18B77D",.3)}{rings(700,560,0.85,.3)}{spark(90,300,40)}{logo()}
    <div class="top"><span class="pill p">Future careers: fields you haven't met yet</span></div>
    <div style="position:absolute;left:64px;right:64px;top:300px">
      <span class="pill l">Today's field</span>
      <div class="H" style="font-size:132px;margin-top:28px">{d["f1"]}<br><span class="l">{d["f2"]}</span></div>
      <p style="font:500 38px/1.35 Roboto;margin:34px 0 44px;max-width:860px">{d["line"]}</p>
      <div style="display:grid;gap:14px">{bars}</div>
      <p style="margin-top:40px" class="lime">{d["end"]}</p>
    </div>{foot()}''')

def cities(d):
    cs = "".join(f'<div style="display:flex;align-items:center;gap:14px;font:700 34px/1 Roboto;padding:22px 0;border-bottom:1px solid rgba(255,255,255,.14)"><span style="color:var(--l)">✦</span>{c}</div>' for c in d["cities"])
    return post(f'''{glow(-200,-200,640,"#7847D6",.45)}{glow(640,860,520,"#FF671B",.35)}{logo()}
    <div class="top"><span class="pill">Global network</span></div>
    <div style="position:absolute;left:64px;right:64px;top:240px">
      <div class="H" style="font-size:94px">{d.get("h1", "Opportunities")}<br><span class="o">{d.get("h2", "around the world.")}</span></div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;column-gap:40px;margin:46px 0 46px">{cs}</div>
      <div class="bar g" style="height:88px;font-size:30px">{d["end"]}</div>
    </div>{foot()}''')

def study(d):
    cols = ["#18B77D", "#7847D6", "#FF671B"]
    rows = "".join(f'<div class="row" style="--c:{cols[k]};font-size:32px"><i>{k+1}</i><span>{x}</span></div>' for k, x in enumerate(d["rows"]))
    return post(f'''{glow(560,-200,600,"#FF671B",.4)}{glow(-200,800,560,"#7847D6",.4)}{spark(900,330,44)}{logo()}
    <div class="top"><span class="pill">{d["tag"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;top:270px">
      <div class="H" style="font-size:118px">{d["h1"]}<br><span class="o">{d["h2"]}</span></div>
      <div style="display:grid;gap:22px;margin:50px 0 46px">{rows}</div>
      <span class="lime" style="font-size:34px">{d["end"]}</span>
    </div>{foot()}''')

def manifesto(d):
    return post(f'''{glow(-160,-120,620,"#7847D6",.5)}{glow(560,760,620,"#FF671B",.4)}{rings(520,640,1.25,.5)}{spark(940,560,50)}{spark(880,260,36,"#FFF1D4")}{logo()}
    <div class="top"><span class="pill">E4I vision</span></div>
    <div style="position:absolute;left:64px;right:64px;top:300px">
      <div style="font:400 200px/.6 'Archivo Black';color:var(--l);height:90px">“</div>
      <div class="H" style="font-size:112px">{d["l1"]}<br>{d["l2"]}<br><span class="o">{d["l3"]}</span></div>
      <p style="font:500 34px/1.4 Roboto;margin:40px 0 46px;max-width:820px;opacity:.9">{d["tr"]}</p>
      <span class="cta">{d.get("cta","Follow for global opportunities.")}</span>
    </div>{foot()}''')

def library():
    n = 4
    return [
      ("01-program-spotlight", program(dict(tag="Program spotlight", h="48 hours.<br>From idea<br><span class='o'>to prototype.</span>",
        bars=[("g", "Format", "Team hackathon"), ("p", "Who", "High school & university"), ("o", "Focus", "AI · Life sciences · Startups")], cta="Apply via link in bio"))),
      ("02-playbook-1-kapak", play_cover(dict(n=n, tag="A 3-step playbook", h="How to land<br>your first<br><span class='o'>internship.</span>", steps=["Map", "Prove", "Ask"]))),
      ("02-playbook-2", play_step(dict(n=n, i=1, step="Map", h1="Before", h2="you apply.", rows=["List 10 teams you admire.", "Find one problem they have.", "Write it in one line."], end="Curiosity beats credentials."))),
      ("02-playbook-3", play_step(dict(n=n, i=2, step="Prove", h1="Prove it", h2="small.", rows=["Build one tiny project.", "Share it in public.", "Ask for one piece of feedback."], end="Proof beats promises."))),
      ("02-playbook-4", play_step(dict(n=n, i=3, step="Ask", h1="Send", h2="the email.", rows=["Five sentences. No more.", "Link the project.", "End with one clear ask."], end="Save this playbook.", btn=True))),
      ("03-future-careers", field(dict(f1="Synthetic", f2="biology", line="Designing living systems the way engineers design machines.",
        bars=[("g", "Skills", "Biology + code + design"), ("p", "Where", "Health · Climate · Food"), ("o", "Start", "A summer lab project")], end="Today's field: tomorrow's career."))),
      ("04-global-network", cities(dict(cities=["San Francisco", "Boston", "New York", "Toronto", "London", "Dublin", "Amsterdam", "Berlin", "Milan", "Geneva", "Dubai", "Istanbul"], end="12 cities. One network."))),
      ("05-study-smarter", study(dict(tag="Study tip", h1="Study smarter,", h2="not longer.", rows=["Review after 1, 3 and 7 days.", "Test yourself before you reread.", "Sleep on it."], end="Spaced repetition beats cramming."))),
      ("06-manifesto", manifesto(dict(l1="Innovation", l2="isn't a talent.", l3="It's a mindset.", tr="İnovasyon bir yetenek değil, geliştirilebilen bir zihniyettir."))),
    ]

META = dict(
  brand="e4i", lang="en",
  intro="Six series built on the logo's colours: green, purple and orange always appear in that order. Every post opens a door: a program, a skill, a field or a city.",
  constants=["Logo on a white tile, top right", "Green contact band with the foundation's own phone line", "Bars always green → purple → orange; lime only for one phrase", "Archivo Black (Arial Black family) for every headline"],
  series=[
    dict(id="01", name="Program Spotlight", img=["01-program-spotlight"], when="Announcing an E4I program: hackathon, internship, competition.", freq="Monthly · around applications", fmt="Single · art band",
      slots=["Art band: grid, glow, logo rings", "Purple tag + 3-line headline (last line orange)", "Three bars: format, who, focus", "Lime outline CTA"],
      caption="48 hours. From idea to prototype. 🚀\n\nThe E4I Hackathon brings high school and university students together around AI, life sciences and startups.\n\nApply via the link in bio.\n#E4I #Hackathon #Innovation #StudentOpportunities"),
    dict(id="02", name="Playbook", img=["02-playbook-1-kapak", "02-playbook-2", "02-playbook-3", "02-playbook-4"], when="A skill taught in three steps; the most saved format.", freq="Every 2 weeks", fmt="Carousel · 4 slides",
      slots=["Cover: question headline + Map/Prove/Ask bars", "Step slides: cream step pill, 2-line headline", "Three numbered rows in green, purple, orange", "Lime lesson line; last slide “Save this playbook.”"],
      caption="Your first internship doesn't start with a CV. It starts with curiosity. 💡\n\n🔹 Map the teams you admire  🔹 Prove it small  🔹 Ask clearly\n\nSave this playbook and tag the friend who's applying this year!\n#E4I #Internship #CareerTips #StudentOpportunities"),
    dict(id="03", name="Future Careers", img=["03-future-careers"], when="Introducing a field students haven't met yet.", freq="Every 2 weeks", fmt="Single · dark",
      slots=["Purple series tag + lime “Today's field”", "Field name, second word lime", "One-line definition", "Three bars: skills, where, start"],
      caption="Today's field: Synthetic Biology 🧬\n\nDesigning living systems the way engineers design machines. Biology, code and design in one career.\n\nWhich field should we cover next?\n#E4I #FutureCareers #SyntheticBiology #STEM"),
    dict(id="04", name="Global Network", img=["04-global-network"], when="Showing the foundation's international reach.", freq="Monthly", fmt="Single · dark",
      slots=["Two-line headline, second line orange", "12-city grid with lime ✦", "Green summary bar"],
      caption="From San Francisco to Istanbul: 12 cities, one network. 🌍\n\nOur students meet the world's innovation ecosystems where they actually happen.\n#E4I #GlobalOpportunities #Innovation"),
    dict(id="05", name="Study Smarter", img=["05-study-smarter"], when="A quick, evidence-based study tip.", freq="Weekly", fmt="Single · dark",
      slots=["Tag + 2-line headline", "Three numbered rows", "Lime closing rule"],
      caption="Study smarter, not longer. 📚\n\nReview after 1, 3 and 7 days, test yourself before you reread, and sleep on it. Spaced repetition beats cramming.\n#E4I #StudyTips #StudentLife"),
    dict(id="06", name="Manifesto", img=["06-manifesto"], when="Repeating the foundation's vision; anchors the grid.", freq="Monthly", fmt="Single · rings",
      slots=["Lime quote mark", "Three-line statement, last line orange", "Turkish translation line", "Lime outline follow CTA"],
      caption="Innovation isn't a talent. It's a mindset. ✨\n\nİnovasyon bir yetenek değil, geliştirilebilen bir zihniyettir.\n#E4I #EducationForInnovation #Innovation"),
  ],
  calendar=[("Mon","Study Smarter","Spaced repetition"),("Tue","Future Careers","Synthetic biology"),("Wed","Playbook","First internship"),("Thu","Program Spotlight","E4I Hackathon"),("Fri","Reels","Event highlights"),
            ("Mon","Study Smarter","Active recall"),("Tue","Global Network","12 cities"),("Wed","Future Careers","AI ethics"),("Thu","Playbook","Winning a pitch"),("Fri","Manifesto","Vision")],
  hooks=["What is a …?", "One opportunity can change your direction.", "Fields you haven't met yet: …", "How to … : a 3-step playbook", "… beats …", "48 hours. From idea to prototype.", "Speed alone isn't progress.", "Save this before …", "Today's field: …", "Problem. People. Plan."],
  ctas=["Save this playbook.", "Tag the person you'd build with.", "Apply via link in bio.", "Follow for global opportunities.", "Read the blog →"],
)


# ---------- Instagram Story (1080×1920) ----------
def story(d):
    """Story: üstte halka grafikli sanat bandı, beyaz + turuncu başlık, lime konturlu CTA. d: tag, title[list], body, cta"""
    lines = d["title"]; n = len(lines)
    t = "".join(f'<span class="o" style="display:block;white-space:nowrap">{x}</span>' if k == n - 1 else f'<span style="display:block;white-space:nowrap">{x}</span>' for k, x in enumerate(lines))
    return doc(CSS, f'''<div class="post"><div class="art" style="height:760px">{grid()}{glow(80,120,520,"#7847D6",.55)}{glow(600,260,460,"#FF671B",.45)}{rings(470,170,1.25,.85)}{spark(140,300,52)}{spark(880,620,40)}{spark(420,520,30,"#FFF1D4")}</div>
    <img class="logo" src="{LOGO}" style="top:220px">
    <div style="position:absolute;left:72px;top:250px"><span class="pill p">{d["tag"]}</span></div>
    <div style="position:absolute;left:72px;right:72px;top:640px;bottom:300px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start">
      <div class="H" style="font-size:104px">{t}</div>
      <p style="font:400 40px/1.42 Roboto;margin:44px 0 56px;opacity:.92">{d["body"]}</p>
      <span class="cta" style="font-size:28px;padding:28px 46px">{d["cta"]}</span>
    </div>
    <div class="foot" style="height:104px"><span>{SITE}</span><span style="opacity:.5">•</span><span>{TEL}</span></div></div>''', lang="en", h=1920)


# ---------- Görünüm temaları (Brand Kit paleti içinde zemin seçenekleri) ----------
THEMES = {
  "koyu": {"name": "Gece laciverti", "css": """
.post.th-koyu{background:var(--n)!important}"""},
  "mor": {"name": "Mor gradyan", "css": """
.post.th-mor{background:linear-gradient(165deg,#5E2390 0%,#3A1670 55%,#1A0E40 100%)!important}
.th-mor .art{background:linear-gradient(135deg,#7847D6 0%,#5E2390 60%,#3A1670 100%)!important}
.th-mor .card{background:rgba(26,14,64,.88)!important}"""},
  "acik": {"name": "Açık zemin (web sitesi gibi)", "css": """
.post.th-acik{background:#F4F6FA!important;color:#15203A!important}
.th-acik .glow{opacity:.14!important}
.th-acik .lime,.th-acik .H .l,.th-acik [style*="color:var(--l)"]{color:#17A26B!important}
.th-acik .cta{color:#15203A!important;box-shadow:inset 0 0 0 3px #17A26B!important}
.th-acik .cta.cr{background:#15203A!important;color:#fff!important;box-shadow:none!important}
.th-acik .card{background:#fff!important;color:#15203A!important;box-shadow:0 10px 30px rgba(21,32,58,.08),inset 0 0 0 2px rgba(21,32,58,.08)!important}
.th-acik .row{color:#15203A}.th-acik .row i,.th-acik .bar{color:#fff}
.th-acik .pill:not(.p):not(.l){background:#15203A!important;color:#fff!important}
.th-acik .dots i{background:rgba(21,32,58,.2)}"""},
}


# ---------- Yeni kompozisyon aileleri ----------
PHOTO_SLOT = {"spotlight"}

ICONS = {
 "bulb": '<path d="M24 6a12 12 0 0 0-7 22v5h14v-5A12 12 0 0 0 24 6zM18 38h12M20 43h8" />',
 "people": '<circle cx="17" cy="16" r="6"/><circle cx="32" cy="18" r="5"/><path d="M6 40c1-8 6-12 11-12s10 4 11 12M27 40c1-6 4-9 7-9s7 3 8 9"/>',
 "list": '<rect x="8" y="6" width="32" height="38" rx="4"/><path d="M15 16h18M15 24h18M15 32h12"/>',
 "cube": '<path d="M24 5 41 14v20L24 43 7 34V14z"/><path d="M7 14l17 9 17-9M24 23v20"/>',
 "flag": '<path d="M10 44V6M10 8h26l-6 9 6 9H10"/>',
 "spark": '<path d="M24 4v12M24 32v12M4 24h12M32 24h12M10 10l8 8M30 30l8 8M38 10l-8 8M18 30l-8 8"/>',
}

def process(d):
    """Seri: Süreç İnfografiği — başlık + ikonlu, bağlantılı adım akışı (blog kapağı / 'Problem → Pitch' dili).
    d: kicker, h1, h2, line, steps[list 4-5]"""
    cols = ["#18B77D", "#7847D6", "#3B82F6", "#FF671B", "#B0FE25"]
    keys = ["bulb", "people", "list", "cube", "flag"]
    n = len(d["steps"]); gap = 952 / n
    nodes = "".join(
        f'<div style="position:absolute;left:{64 + k*gap}px;width:{gap}px;top:0;text-align:center">'
        f'<div style="margin:0 auto;width:150px;height:150px;border-radius:50%;background:#0B1730;box-shadow:inset 0 0 0 4px {cols[k]},0 0 40px {cols[k]}55;display:grid;place-items:center">'
        f'<svg width="70" height="70" viewBox="0 0 48 48" fill="none" stroke="{cols[k]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{ICONS[keys[k % 5]]}</svg></div>'
        f'<div style="font:400 27px/1.15 \'Archivo Black\';text-transform:uppercase;margin-top:24px;color:{cols[k]}">{s}</div></div>'
        for k, s in enumerate(d["steps"]))
    return post(f'''{grid().replace('height="470"','height="1350"').replace('width="1080" height="470"','width="1080" height="1350"')}{glow(-200,-160,620,"#7847D6",.45)}{glow(620,700,560,"#18B77D",.28)}{logo()}
    <div style="position:absolute;left:64px;top:84px;font:700 22px/1 Roboto;letter-spacing:.24em;color:#9FB0D0">{d["kicker"]}</div>
    <div style="position:absolute;left:64px;right:64px;top:250px">
      <div class="H" style="font-size:96px">{d["h1"]}<br><span class="l">{d["h2"]}</span></div>
      <p style="font:500 36px/1.4 Roboto;margin-top:34px;max-width:880px;opacity:.9">{d["line"]}</p></div>
    <div class="deco" style="left:{64 + gap/2}px;right:{64 + gap/2}px;top:983px;height:4px;background:linear-gradient(90deg,#18B77D,#7847D6,#FF671B)"></div>
    <div style="position:absolute;left:0;right:0;top:908px;height:300px">{nodes}</div>
    {foot()}''')

def spotlight(d):
    """Seri: Innovation Spotlight — üstte geniş görsel alan (fotoğraf ya da neon ağ grafiği), altta kart: etiket, iki renkli başlık, iki hap.
    d: tag, h1, h2, sub, chips[2], photo(isteğe bağlı)"""
    art = (f'<div style="position:absolute;left:0;right:0;top:0;height:760px;overflow:hidden;background:linear-gradient(160deg,#1A1145 0%,#0B1A3A 60%,#2A1408 100%)">'
           f'{grid().replace("470","760")}{glow(-80,200,520,"#7847D6",.6)}{glow(620,60,460,"#FF671B",.5)}{rings(300,120,1.2,.9)}'
           f'{spark(160,140,52)}{spark(860,520,40)}{spark(700,180,30,"#FFF1D4")}</div>')
    vis = f'<img src="{d["photo"]}" style="position:absolute;left:0;right:0;top:0;width:100%;height:760px;object-fit:cover">' if d.get("photo") else art
    chips = "".join(f'<span class="pill" style="background:transparent;box-shadow:inset 0 0 0 3px var(--l);color:#fff">{c}</span>' for c in d["chips"])
    return post(f'''{vis}<div class="deco" style="left:0;right:0;top:560px;height:220px;background:linear-gradient(180deg,rgba(5,14,31,0),#050E1F)"></div>{logo()}
    <div style="position:absolute;left:64px;right:64px;top:700px">
      <span class="pill p">{d["tag"]}</span>
      <div class="H" style="font-size:92px;margin-top:26px">{d["h1"]}<br><span class="o">{d["h2"]}</span></div>
      <p style="font:500 34px/1.38 Roboto;margin:26px 0 30px;max-width:900px;opacity:.92">{d["sub"]}</p>
      <div style="display:flex;gap:14px;flex-wrap:wrap">{chips}</div>
    </div>{foot()}''')


# ---------- Kütüphane: yeni kompozisyon aileleri ve Story ----------
_LIB0 = library
def library():
    return _LIB0() + [
      ("07-process", process(dict(kicker="EDUCATION FOR INNOVATION", h1="What is a", h2="hackathon?",
        line="From a real problem to a working prototype, in five moves.", steps=["Problem", "People", "Plan", "Prototype", "Pitch"]))),
      ("08-spotlight", spotlight(dict(tag="Innovation spotlight", h1="Robots that", h2="learn by watching.",
        sub="Imitation learning lets machines copy a task from a few human demonstrations.", chips=["AI + robotics", "Try: a simulation lab"]))),
      ("09-story", story(dict(tag="Study tip", title=["Review", "after 1, 3", "and 7 days."],
        body="Spaced repetition beats cramming. Test yourself before you reread.", cta="Save this story"))),
    ]

META["intro"] = ("Eight feed series and one Story layout, each a different composition family: art-band announcement, playbook carousel, "
                 "field card, city grid, numbered tips, manifesto, icon process infographic and a photo-led spotlight. "
                 "The logo sits top right without a tile, exactly as on Instagram.")
META["constants"] = ["Logo top right, no tile (as on Instagram)", "Green contact band: educationforinnovation.org • +90 212 287 8606",
                     "Bars always green → purple → orange; lime only for one phrase", "Archivo Black (Arial Black family) for every headline"]
META["series"] += [
  dict(id="07", name="Process Infographic", img=["07-process"], when="Explaining how something works as a flow of 4–5 steps (blog cover language).",
       freq="Monthly · with blog posts", fmt="Single · icon flow",
       slots=["Small spaced kicker", "Two-line headline, second line lime", "One-line promise", "4–5 neon icon nodes on a gradient line, labels in brand colours"],
       caption="What is a hackathon? 🧩\n\nProblem → People → Plan → Prototype → Pitch. Five moves from a real problem to a working demo.\n\nRead the full guide on our blog.\n#E4I #Hackathon #Innovation #StudentOpportunities"),
  dict(id="08", name="Innovation Spotlight", img=["08-spotlight"], when="Introducing a technology or idea with a strong visual; photo-led when a photo is available.",
       freq="Every 2 weeks", fmt="Single · large visual",
       slots=["Top 55%: uploaded photo or neon grid + logo rings", "Purple tag", "Two-line headline, second line orange", "Two lime-outline chips (field + first step)"],
       caption="Robots that learn by watching. 🤖\n\nImitation learning lets machines copy a task from a handful of human demonstrations. A field where AI meets robotics.\n#E4I #FutureCareers #Robotics #AI"),
  dict(id="09", name="Instagram Story", img=["09-story"], when="A one-screen reminder supporting a feed post; 1080×1920.",
       freq="With feed posts", fmt="Story · 9:16",
       slots=["Safe zones top and bottom", "Art band with logo rings", "White + orange headline", "Lime outline CTA"],
       caption="Stories have no caption; highlight note: “Study tips.” #E4I"),
]
