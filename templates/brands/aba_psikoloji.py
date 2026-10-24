"""ABA Psikoloji post şablonları (1080×1350)."""
from engine import doc, asset
LOGO = asset("aba-psikoloji/logo-mark-white.png")
SITE, TEL, MAIL = "abapsikoloji.com", "+90 545 359 66 36", "info@abapsikoloji.com"

CSS = """
:root{--o:#F48011;--oc:#F26F12;--od:#E64E03;--b:#A6264C;--bd:#7E243C;--s:#577D66;--s5:#DCE6DF;--c:#FFF7EB;--pe:#F8D6A8;--p5:#FFE8CD;--ch:#1B1817;--cc:#2C2A29;--k:#211E1C}
.post{font-family:Montserrat;color:var(--k);background:var(--c)}
.dk{background:var(--ch);color:#fff}
.deco{position:absolute;pointer-events:none}
.circ{position:absolute;border-radius:50%}
.tile{position:absolute;right:64px;top:64px;width:112px;height:112px;border-radius:24px;background:var(--o);display:grid;place-items:center}.tile img{width:70px}
.tag{display:inline-block;padding:13px 30px;border-radius:99px;background:var(--b);color:#fff;font:700 22px/1 Montserrat;letter-spacing:.06em;text-transform:uppercase}
.tag.s{background:var(--s)}.tag.o{background:var(--oc)}.tag.k{background:var(--ch)}
.top{position:absolute;left:64px;top:96px}
.foot{position:absolute;left:0;right:0;bottom:0;height:96px;background:var(--o);color:var(--k);display:flex;justify-content:center;align-items:center;gap:30px;font:600 24px/1 Montserrat}
.foot i{font-style:normal;opacity:.6}
.h{font:800 92px/1.0 Montserrat;text-transform:uppercase;letter-spacing:-.01em}
.h .b{color:var(--b)}.h .o{color:var(--o)}.h .s{color:var(--s)}
.rule{width:240px;height:8px;border-radius:4px;background:var(--s);margin:34px 0}
.rule.b{background:var(--b)}
.card{border-radius:40px;padding:44px 52px;background:#fff;box-shadow:inset 0 0 0 3px #EEDFCB}
.card p{font:600 31px/1.42 Montserrat}.card b{color:var(--b);font-weight:800}
.glass{border-radius:40px;padding:44px 52px;background:var(--cc);box-shadow:inset 0 0 0 3px rgba(255,255,255,.18)}
.glass p{font:600 35px/1.42 Montserrat;color:#fff}.glass b{color:var(--o);font-weight:800}
.lbl{font:800 24px/1 Montserrat;letter-spacing:.08em;text-transform:uppercase;margin-bottom:18px}
.quote{border-radius:32px;background:var(--b);color:#fff;padding:34px 44px;font:800 40px/1.2 Montserrat;text-transform:uppercase}
.cta{display:inline-flex;align-items:center;gap:14px;padding:24px 44px;border-radius:99px;background:var(--oc);color:#fff;font:800 25px/1 Montserrat;letter-spacing:.04em;text-transform:uppercase}
.cta.ol{background:#fff;color:var(--oc);box-shadow:inset 0 0 0 4px var(--oc)}
.cta.bu{background:var(--b)}
.qbox{display:inline-block;background:var(--oc);color:#fff;border-radius:22px;padding:30px 38px;font:800 50px/1.12 Montserrat;text-transform:uppercase}
.dots{position:absolute;bottom:128px;left:0;right:0;display:flex;justify-content:center;gap:12px}.dots i{width:12px;height:12px;border-radius:50%;background:rgba(0,0,0,.18)}.dots i.on{background:var(--o);width:34px;border-radius:6px}
.dk .dots i{background:rgba(255,255,255,.25)}
.swipe{font:800 24px/1 Montserrat;letter-spacing:.06em;color:var(--b);text-transform:uppercase}
.myth,.fact{border-radius:40px;padding:40px 52px 50px;position:relative}
.myth{background:var(--b);color:#fff}.fact{background:#fff;box-shadow:inset 0 0 0 5px var(--s)}
.myth blockquote,.fact blockquote{font:800 40px/1.24 Montserrat;margin-top:26px}
.fact small{display:block;font:700 26px/1.35 Montserrat;color:var(--b);margin-top:18px}
.vs{position:absolute;left:50%;transform:translate(-50%,-50%);width:112px;height:112px;border-radius:50%;background:var(--c);box-shadow:inset 0 0 0 5px var(--o);display:grid;place-items:center;font:800 32px/1 Montserrat;color:var(--o);z-index:2}
.nb{border-radius:30px;background:#fff;padding:44px 44px;box-shadow:inset 0 0 0 3px var(--o)}
.nb.s{box-shadow:inset 0 0 0 3px var(--s)}.nb.b{box-shadow:inset 0 0 0 3px var(--b)}
.nb header{display:flex;align-items:center;gap:20px;font:800 34px/1 Montserrat;text-transform:uppercase;margin-bottom:16px}
.nb .n{width:58px;height:58px;border-radius:14px;display:grid;place-items:center;background:var(--oc);color:#fff;font:800 30px/1 Montserrat}
.nb.s .n{background:var(--s)}.nb.b .n{background:none;color:var(--b);font-size:58px;width:auto}
.nb p{font:600 32px/1.45 Montserrat}
.chips{display:flex;flex-wrap:wrap;gap:16px}.chip{padding:22px 32px;border-radius:14px;color:#fff;font:800 28px/1 Montserrat;text-transform:uppercase;background:var(--oc)}
.chip.s{background:var(--s)}.chip.b{background:var(--b)}.chip.k{background:var(--ch)}
.dl{list-style:none;display:grid;gap:22px;font:800 34px/1 Montserrat;text-transform:uppercase}.dl li{display:flex;align-items:center;gap:22px}.dl li::before{content:"";width:26px;height:26px;border-radius:50%;background:var(--c2,var(--o))}
.steps{display:grid;gap:22px}.st{display:flex;gap:22px;align-items:flex-start;font:600 30px/1.38 Montserrat}.st i{flex:none;width:52px;height:52px;border-radius:50%;background:var(--o);color:#fff;display:grid;place-items:center;font:800 26px/1 Montserrat;font-style:normal}
.st:nth-child(2) i{background:var(--b)}.st:nth-child(3) i{background:var(--s)}
.serif{font-family:'Playfair Display';font-weight:800;letter-spacing:-.02em}
"""

def flower(x, y, r, color, w=3, op=1):
    pts = [(0, -0.95), (0.9, -0.29), (0.56, 0.77), (-0.56, 0.77), (-0.9, -0.29)]
    cs = "".join(f'<circle cx="{r*1.05+px*r*0.62:.1f}" cy="{r*1.05+py*r*0.62:.1f}" r="{r*0.62:.1f}" fill="none" stroke="{color}" stroke-width="{w}"/>' for px, py in pts)
    s = r * 2.1
    return f'<svg class="deco" style="left:{x}px;top:{y}px;opacity:{op}" width="{s:.0f}" height="{s:.0f}">{cs}</svg>'

def circ(x, y, d, color):
    return f'<div class="deco circ" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;background:{color}"></div>'

def tile(): return f'<div class="tile"><img src="{LOGO}"></div>'
def foot(): return f'<div class="foot">{SITE}<i>•</i>{TEL}<i>•</i>{MAIL}</div>'
def dots(n, i): return '<div class="dots">' + "".join(f'<i class="{"on" if k==i else ""}"></i>' for k in range(n)) + "</div>"
def post(inner, cls=""): return doc(CSS, f'<div class="post {cls}">{inner}</div>')

# ---------- Şablonlar ----------
def ic_ses(d):
    """Seri: İç Ses — koyu kart. d: tag, quote[list], label, body(html), cta"""
    q = "<br>".join(d["quote"])
    return post(f'''{flower(-120,-150,330,"#F48011",3,.35)}{flower(820,1010,240,"#A6264C",3,.5)}{tile()}
    <div class="top"><span class="tag">{d["tag"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;top:270px">
      <div style="font:800 150px/0.6 'Playfair Display';color:var(--o);height:70px">“</div>
      <div class="h" style="font-size:100px;color:#fff">{q}</div>
      <div class="rule" style="background:var(--o)"></div>
      <div class="glass"><div class="lbl" style="color:var(--o)">{d["label"]}</div><p>{d["body"]}</p></div>
      <div style="margin-top:44px"><span class="cta">{d["cta"]} →</span></div>
    </div>{foot()}''', "dk")

def ebeveyn(d):
    """Seri: Ebeveyn Rehberi — krem, soru kutusu. d: headline[list], q, body, cta"""
    return post(f'''{circ(640,-260,620,"#F8D6A8")}{circ(-200,980,460,"#FFE8CD")}{flower(700,880,210,"#A6264C",3,.35)}{tile()}
    <div class="top"><span class="tag">Ebeveyn Rehberi</span></div>
    <div style="position:absolute;left:64px;right:64px;top:250px">
      <div class="h" style="font-size:76px">{"<br>".join(d["headline"])}</div>
      <div style="margin-top:30px"><span class="qbox">{d["q"]}</span></div>
      <div class="rule b"></div>
      <div class="card" style="margin-right:90px"><p>{d["body"]}</p></div>
      <div style="margin-top:42px"><span class="cta ol">{d["cta"]} →</span></div>
    </div>{foot()}''')

def mit_kapak(d):
    return post(f'''{circ(-180,-200,520,"#F8D6A8")}{circ(820,700,420,"#DCE6DF")}{circ(880,140,140,"#E9DDF2")}{tile()}
    <div class="top"><span class="tag s">{d["tag"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;top:270px;text-align:center">
      <div class="h" style="font-size:118px">{d["l1"]}<br><span class="b">{d["l2"]}</span><br><span class="o">{d["l3"]}</span></div>
      <div class="rule" style="margin:36px auto"></div>
      <div style="font:800 44px/1.15 Montserrat;text-transform:uppercase">İKİ DÜŞÜNCE.<br><span style="color:var(--s)">HANGİSİ GERÇEK?</span></div>
      <div class="card" style="margin:40px 70px 0"><p style="font-size:29px">{d["body"]}</p></div>
      <div style="margin-top:38px"><span class="cta">{d.get("cta","BİRLİKTE AYIRALIM →")}</span></div>
    </div>{dots(d["n"],0)}{foot()}''')

def mit_sayfa(d):
    return post(f'''{circ(-240,820,420,"#DCE6DF")}{circ(860,-120,300,"#F8D6A8")}{tile()}
    <div class="top"><span class="tag">MİT {d["i"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;top:210px">
      <div class="h" style="font-size:58px;margin-bottom:30px">İKİ DÜŞÜNCE<br><span class="b">KARŞI KARŞIYA</span></div>
      <div style="position:relative">
        <div class="myth"><span class="tag k">MİT</span><blockquote>“{d["myth"]}”</blockquote></div>
        <div class="vs" style="top:50%">VS</div>
        <div class="fact" style="margin-top:34px"><span class="tag s">GERÇEK</span><blockquote>“{d["fact"]}”</blockquote><small>{d["note"]}</small></div>
      </div>
      <div style="text-align:center;margin-top:34px" class="swipe">{d.get("swipe","BİR SONRAKİ MİT İÇİN KAYDIR →")}</div>
    </div>{dots(d["n"],d["i"])}{foot()}''')

def kapanis(d):
    cols = ["#F48011", "#A6264C", "#577D66", "#F2A93B", "#F26F12"]
    li = "".join(f'<li style="--c2:{cols[k%5]}">{x}</li>' for k, x in enumerate(d["list"]))
    return post(f'''{circ(700,-220,560,"#F8D6A8")}{circ(-180,760,360,"#DCE6DF")}{tile()}
    <div class="top"><span class="tag o">{d["tag"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;top:250px">
      <div class="h" style="font-size:104px">ŞİMDİ<br><span class="o">SIRA SENDE</span></div>
      <p style="font:600 32px/1.4 Montserrat;margin:30px 120px 40px 0">{d["body"]}</p>
      <ul class="dl">{li}</ul>
      <div style="margin-top:56px;border-radius:36px;background:var(--ch);color:#fff;padding:36px 44px;display:flex;justify-content:space-between;align-items:center">
        <div style="font:800 34px/1.2 Montserrat;text-transform:uppercase">{d["box"]}</div><span class="cta bu" style="padding:20px 32px;font-size:22px">{d["cta"]}</span></div>
    </div>{dots(d["n"],d["n"]-1)}{foot()}''')

def pasaport_kapak(d):
    return post(f'''{circ(-160,-160,420,"#F8D6A8")}{tile()}
    <div class="top"><span class="tag">SINAV PASAPORTU · BUGÜNKÜ DURAK</span></div>
    <div style="position:absolute;left:64px;right:64px;top:250px;border-radius:44px;background:#fff;box-shadow:inset 0 0 0 3px #EEDFCB;padding:56px 60px 60px;height:860px">
      <div style="display:flex;gap:40px;align-items:center">
        <div style="width:250px;height:330px;border-radius:24px;background:var(--bd);position:relative;flex:none;display:grid;place-items:center">
          {flower(30,40,90,"#F8D6A8",3,.9).replace('class="deco"','class="deco" ')}
          <div style="position:absolute;bottom:34px;left:0;right:0;text-align:center;font:800 20px/1.3 Montserrat;color:#F8D6A8;letter-spacing:.14em">SINAV<br>PASAPORTU</div></div>
        <div><div style="font:800 170px/0.9 Montserrat;letter-spacing:-.03em">{d["code"]}</div>
          <div style="font:800 26px/1.3 Montserrat;color:var(--bd);text-transform:uppercase;margin-top:16px">{d["full"]}</div></div>
      </div>
      <p style="font:600 32px/1.42 Montserrat;margin:44px 0 36px">{d["desc"]}</p>
      <span style="display:inline-block;padding:18px 30px;border-radius:99px;box-shadow:inset 0 0 0 4px var(--o);color:var(--oc);font:800 28px/1 Montserrat">{d["pill"]}</span>
      <div style="position:absolute;left:60px;bottom:54px;font:800 32px/1 Montserrat;color:var(--b)">{d.get("link","Pasaportu aç →")}</div>
      <div style="position:absolute;right:56px;top:-6px;bottom:-6px;border-right:4px dashed #F8C48C"></div>
    </div>{dots(3,0)}{foot()}''')

def pasaport_ic(d):
    bx = d["boxes"]
    return post(f'''{tile()}
    <div class="top"><span class="tag s">{d["code"]} PASAPORTU</span></div>
    <div style="position:absolute;left:64px;right:64px;top:250px;display:grid;gap:36px">
      <div class="nb"><header><span class="n">1</span>{bx[0][0]}</header><p>{bx[0][1]}</p></div>
      <div class="nb s"><header><span class="n">2</span>{bx[1][0]}</header><p>{bx[1][1]}</p></div>
      <div class="nb b" style="background:#FFF"><header><span class="n">03</span>{bx[2][0]}</header><p>{bx[2][1]}</p></div>
    </div>{dots(3,1)}{foot()}''')

def pasaport_son(d):
    cl = ["", "s", "b", "k"]
    ch = "".join(f'<span class="chip {cl[k]}" lang="en">{x}</span>' for k, x in enumerate(d["chips"]))
    return post(f'''{circ(720,-240,560,"#F8D6A8")}{tile()}
    <div class="top"><span class="tag">SINAV PASAPORTU</span></div>
    <div style="position:absolute;left:64px;right:64px;top:330px">
      <div class="h" style="font-size:88px">{d["q"]}</div>
      <div class="rule"></div>
      <div class="chips">{ch}</div>
      <p style="font:700 34px/1.3 Montserrat;margin:44px 0">{d.get("ask","Yorumlara yaz. 👇")}</p>
      <span class="cta">{d.get("cta","ABA PSİKOLOJİ İLE İLETİŞİME GEÇ")}</span>
    </div>{dots(3,2)}{foot()}''')

def rutin(d):
    st = "".join(f'<div class="st"><i>{k+1}</i><span>{x}</span></div>' for k, x in enumerate(d["steps"]))
    return post(f'''{circ(-220,-220,560,"#F8D6A8")}{circ(860,1000,320,"#DCE6DF")}{tile()}
    <div class="top"><span class="tag">{d["tag"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;top:240px">
      <div class="h" style="font-size:100px">{d["l1"]}<br><span class="b">{d["l2"]}</span><br><span class="o">{d["l3"]}</span></div>
      <div class="quote" style="margin:34px 160px 30px 0">“{d["voice"]}”</div>
      <div class="card"><div class="steps">{st}</div></div>
      <div style="font:800 30px/1.2 Montserrat;color:var(--s);text-transform:uppercase;margin:30px 0 26px">{d["line"]}</div>
      <span class="cta ol">{d["cta"]} →</span>
    </div>{foot()}''')

def uzman(d):
    return post(f'''<div style="position:absolute;inset:0 0 520px 0;background:#fff"></div>
    <div style="position:absolute;left:0;right:0;bottom:0;height:520px;background:var(--od)"></div>
    {flower(700,820,220,"#FFFFFF",2.5,.35)}{tile()}
    <div style="position:absolute;left:64px;right:220px;top:96px">
      <div style="font:700 24px/1 Montserrat;letter-spacing:.2em;color:var(--od);padding-bottom:22px;border-bottom:3px solid var(--od)">{d["byline"]}</div>
      <div class="serif" style="font-size:86px;line-height:.98;margin-top:36px">{d["title"]}<br><em style="font-style:normal;color:var(--od)">{d["title2"]}</em></div>
    </div>
    <div style="position:absolute;left:64px;right:64px;bottom:150px;color:#fff">
      <div style="font:800 24px/1 Montserrat;letter-spacing:.12em;opacity:.85;margin-bottom:20px">BU YAZIDA</div>
      <div class="serif" style="font-size:50px;line-height:1.12;max-width:760px">{d["summary"]}</div>
      <div style="margin-top:36px;font:800 28px/1 Montserrat">{d.get("cta","Blog yazımızı inceleyiniz →")}</div>
    </div>{foot()}''')

# ---------- Örnek içerik ----------
def library():
    n = 4
    return [
      ("01-ic-ses", ic_ses(dict(tag="İç ses", quote=["Herkes benden", "daha hızlı", "ilerliyor."], label="Karşılaştırma",
        body="Bu düşünce yetersizlik değil; <b>kendi ritmini kaybettiğinin</b> işareti olabilir.", cta="Kendi ritmini birlikte bulalım"))),
      ("02-ebeveyn-rehberi", ebeveyn(dict(headline=["Çocuğunuz sınav", "sonucunu sizden", "saklıyorsa..."], q="Notu mu, yoksa<br>tepkinizi mi?",
        body="Sakladığı şey not değil, <b>sizin tepkinize dair korkusu</b> olabilir. İlk cümleniz “Nasıl hissediyorsun?” olsun.", cta="Birlikte konuşalım"))),
      ("03-mit-1-kapak", mit_kapak(dict(n=n, tag="Doğru bildiğimiz yanlışlar", l1="Sınav", l2="gecesi", l3="mitleri",
        body="Sınav haftasında en sık duyduğumuz iki cümleyi ayırıyoruz."))),
      ("03-mit-2", mit_sayfa(dict(n=n, i=1, myth="Sınavdan önceki gece sabahlarsam daha çok konu yetiştiririm.",
        fact="Uyku, gün içinde öğrendiklerini hafızaya yerleştirir.", note="Son gece yeni konu değil, dinlenmiş bir zihin kazandırır."))),
      ("03-mit-3", mit_sayfa(dict(n=n, i=2, myth="Kaygı hissediyorsam yeterince hazır değilimdir.",
        fact="Orta düzeyde kaygı, dikkati toplamaya yardım eder.", note="Hedef kaygıyı yok etmek değil, yönetmek.", swipe="ÖZET İÇİN KAYDIR →"))),
      ("03-mit-4-kapanis", kapanis(dict(n=n, tag="Sınav haftası", body="Son gece için dört küçük karar, büyük bir fark yaratır.",
        list=["Uyu", "Tekrar et, yükleme", "Nefes al", "Kendine güven"], box="Sınav dönemini<br>birlikte planlayalım", cta="Bize yaz →"))),
      ("04-pasaport-1-kapak", pasaport_kapak(dict(code="IELTS", full="International English<br>Language Testing System",
        desc="Yurt dışında eğitim için en yaygın İngilizce yeterlik sınavlarından biri.", pill="4 BÖLÜM • 0–9 BANT"))),
      ("04-pasaport-2", pasaport_ic(dict(code="IELTS", boxes=[("Kimler için?", "Birleşik Krallık, Avustralya, Kanada ve daha birçok ülkede okumak isteyen öğrenciler."),
        ("Ne ölçer?", "Dinleme, okuma, yazma ve konuşma. Her bölüm ayrı bir bant puanı alır."),
        ("Hazırlık vizesi", "Konuşma bölümündeki kaygı çok yaygındır. Günde 5 dakika sesli pratik, bu kaygıyı küçültür.")]))),
      ("04-pasaport-3", pasaport_son(dict(q="Senin IELTS<br>hazırlığında<br>en zor bölüm hangisi?", chips=["Listening", "Reading", "Writing", "Speaking"]))),
      ("05-haftanin-rutini", rutin(dict(tag="Pazartesi enerjisi", l1="Yeni hafta", l2="yeni bir", l3="plan", voice="Bu hafta her şeye yetişmem lazım.",
        steps=["Haftanın tek önceliğini seç.", "Her güne 25 dakikalık bir blok koy.", "Cuma akşamı neyin işe yaradığını yaz."],
        line="Plan küçüldükçe kaygı da küçülür.", cta="Haftanı birlikte planlayalım"))),
      ("06-uzman-notu", uzman(dict(byline="UZMAN NOTU · ABA PSİKOLOJİ", title="Tercih Döneminde", title2="Kim Konuşuyor, Kim Dinliyor?",
        summary="Tercih konuşmalarında gencin sesine alan açmanın üç yolu."))),
    ]

META = dict(
  brand="aba_psikoloji", lang="tr",
  intro="Altı seri, haftada 4–5 paylaşım. Her seri tek bir ihtiyaca cevap verir ve hep aynı görünür; takipçi postu logoya bakmadan tanır.",
  constants=["Sağ üstte turuncu logo karosu, altta turuncu iletişim bandı", "Tek turuncu (#F48011); bantta okunurluk için koyu metin", "Montserrat; başlık BÜYÜK HARF, en fazla 3 satır", "Sitedeki tek telefon hattı (+90 545 359 66 36)"],
  series=[
    dict(id="01", name="İç Ses", img=["01-ic-ses"], when="Öğrencinin kafasındaki cümleyi yakalayıp yeniden çerçevelemek için.", freq="Haftada 1 · Pazartesi", fmt="Tek post · koyu",
      slots=["Etiket: duygu adı (İç ses / Karşılaştırma)", "Alıntı: birinci tekil cümle, en fazla 3 satır", "Kart: “X değil, Y” cümlesi", "CTA: fiil + “birlikte”"],
      caption="“Herkes benden daha hızlı ilerliyor.” Bu cümleyi hiç kurdun mu? 🌿\n\nKarşılaştırma bir ölçü değil; çoğu zaman kendi ritmini kaybettiğinin işaretidir. Bugün sadece dünkü kendinle kıyasla.\n\nABA Psikoloji ile kendi ritmini birlikte bulalım.\n#ABAPsikoloji #ÖğrenciPsikolojisi #Motivasyon #SınavKaygısı"),
    dict(id="02", name="Ebeveyn Rehberi", img=["02-ebeveyn-rehberi"], when="Velilere tek bir zor anı ve ilk cümleyi vermek için.", freq="Haftada 1 · Çarşamba", fmt="Tek post · krem",
      slots=["Başlık: “Çocuğunuz … ise” durumu", "Turuncu kutu: asıl soru", "Kart: “X değil, Y” + ilk cümle önerisi", "CTA: “Birlikte konuşalım”"],
      caption="Çocuğunuz sınav sonucunu sizden saklıyorsa, sakladığı şey not olmayabilir. 💬\n\nÇoğu zaman gizlenen, sizin tepkinize dair korkudur. Konuşmayı “Kaç aldın?” yerine “Nasıl hissediyorsun?” ile açın.\n\nABA Psikoloji ile bu konuşmayı birlikte planlayalım.\n#ABAPsikoloji #EbeveynRehberi #Aileİletişimi #ÖğrenciPsikolojisi"),
    dict(id="03", name="Mit vs Gerçek", img=["03-mit-1-kapak", "03-mit-2", "03-mit-3", "03-mit-4-kapanis"], when="Yaygın bir yanlışı kaydırmalı bir hikâyeyle düzeltmek için.", freq="2 haftada 1 · Perşembe", fmt="Carousel · 4 sayfa",
      slots=["Kapak: üç renkli başlık (mürekkep / bordo / turuncu)", "Sayfa 2–3: bordo MİT ↔ adaçayı GERÇEK", "Kapanış: “Şimdi sıra sende” + nokta listesi", "Renk kuralı: bordo = mit, adaçayı = gerçek"],
      caption="Sınav gecesi en çok duyduğumuz iki cümle: “Sabahlarsam yetiştiririm” ve “Kaygılıysam hazır değilim.” 📚\n\nİkisini de kaydırarak ayırıyoruz. Uyku öğrendiklerini kalıcı hale getirir; orta düzeyde kaygı ise dikkati toplar.\n\nSınav dönemini ABA Psikoloji ile birlikte planlayalım.\n#ABAPsikoloji #SınavKaygısı #SınavaHazırlık #Uyku"),
    dict(id="04", name="Sınav Pasaportu", img=["04-pasaport-1-kapak", "04-pasaport-2", "04-pasaport-3"], when="Bir sınavı psikolojik açıdan tanıtan seri; her post bir “durak”.", freq="2 haftada 1 · Salı", fmt="Carousel · 3 sayfa",
      slots=["Kapak: sınav kısaltması + açılım + bilgi hapı", "Sayfa 2: numaralı kutular 1–2–03", "03 her zaman “Hazırlık vizesi”: kaygı ve plan", "Kapanış: seçenek çipleri + “Yorumlara yaz”"],
      caption="Sınav Pasaportu'nun bugünkü durağı: IELTS ✈️\n\nDört bölüm, 0–9 bant. Konuşma bölümündeki kaygı çok yaygın; günde 5 dakika sesli pratik bu kaygıyı küçültür.\n\nSenin için en zor bölüm hangisi? Yorumlara yaz 👇\n#ABAPsikoloji #IELTS #SınavPasaportu #YurtDışıEğitim"),
    dict(id="05", name="Haftanın Rutini", img=["05-haftanin-rutini"], when="Gün ve mevsim girişiyle küçük, uygulanabilir bir plan vermek için.", freq="Haftada 1 · Pazartesi / Cuma", fmt="Tek post · krem",
      slots=["Etiket: gün girişi (Pazartesi enerjisi, Sonbahar cuması)", "Üç renkli başlık", "Bordo iç ses kutusu", "3 numaralı adım + adaçayı özet satırı"],
      caption="Yeni hafta, yeni bir plan. 🎯\n\n“Bu hafta her şeye yetişmem lazım” düşüncesi planı büyütür, kaygıyı da. Tek öncelik seç, her güne 25 dakika koy, cuma akşamı neyin işe yaradığını yaz.\n\nHaftanı ABA Psikoloji ile birlikte planlayalım.\n#ABAPsikoloji #ZamanYönetimi #Motivasyon #ÇalışmaPlanı"),
    dict(id="06", name="Uzman Notu", img=["06-uzman-notu"], when="Blog yazısını duyurmak ve kurumun uzmanlığını göstermek için.", freq="Ayda 2 · Blog yayın günü", fmt="Tek post · beyaz + alev turuncu",
      slots=["Byline: yazarın adı ve unvanı (gerçek yazar)", "Serif başlık; son satır alev turuncu", "Alt blok: “Bu yazıda” tek cümle özet", "Footer + “Blog yazımızı inceleyiniz”"],
      caption="Tercih döneminde aile sofrasında kim konuşuyor, kim dinliyor? ✨\n\nYeni blog yazımızda gencin sesine alan açmanın üç yolunu anlattık. Link biyografide.\n#ABAPsikoloji #EbeveynRehberi #KariyerPlanlama #Blog"),
  ],
  calendar=[("Pzt","İç Ses","“Herkes benden hızlı ilerliyor.”"),("Sal","Sınav Pasaportu","IELTS durağı"),("Çar","Ebeveyn Rehberi","Sonucu saklayan çocuk"),("Per","Mit vs Gerçek","Sınav gecesi mitleri"),("Cum","Haftanın Rutini","Sonbahar cuması: dinlenme planı"),
            ("Pzt","Haftanın Rutini","Pazartesi enerjisi: tek öncelik"),("Sal","Uzman Notu","Blog: tercih döneminde aile"),("Çar","Ebeveyn Rehberi","Motivasyon mu, baskı mı?"),("Per","İç Ses","“Yanlış bölümü seçersem?”"),("Cum","Reels","Open Day hatırlatma (Pazar 18.00)")],
  hooks=["“… cümlesini hiç kurdun mu?”", "Bu kaygı başarısızlık değil, …", "Çocuğunuz … ise, ilk cümleniz şu olsun:", "Doğru bildiğimiz yanlışlar: …", "Sınav Pasaportu'nun bugünkü durağı: …", "Yeni hafta. Yeni bir plan.", "Kararsızlık bazen tembellik değil, …", "Sorun her zaman disiplin değildir.", "Motivasyon vermeye çalışırken …", "Sonbahar cuması: …"],
  ctas=["… birlikte planlayalım →", "Kaygıyı birlikte küçültelim →", "Birlikte ayıralım →", "Birlikte konuşalım →", "Yorumlara yaz 👇", "Blog yazımızı inceleyiniz →"],
)


# ---------- Instagram Story (1080×1920) ----------
# Güvenli alan: üst ~250 px ve alt ~280 px Instagram arayüzüyle örtüşebilir; ana metin bu bandın dışında tutulur.
def story(d):
    """Story: krem zemin, üç renkli başlık, beyaz kart, CTA. d: tag, title[list], body(html), cta"""
    cols = ["", "b", "o", ""]
    lines = d["title"]; n = len(lines)
    t = "".join(f'<span class="{"o" if k == n - 1 else cols[k % 2]}" style="display:block;white-space:nowrap">{x}</span>' for k, x in enumerate(lines))
    return doc(CSS, f'''<div class="post">{circ(560,-200,700,"#F8D6A8")}{circ(-260,1420,620,"#FFE8CD")}{circ(860,1180,300,"#DCE6DF")}
    {flower(640,1380,240,"#A6264C",3,.35)}<div class="tile" style="top:220px">{f'<img src="{LOGO}">'}</div>
    <div style="position:absolute;left:72px;top:250px"><span class="tag">{d["tag"]}</span></div>
    <div style="position:absolute;left:72px;right:72px;top:380px;bottom:300px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start">
      <div class="h" style="font-size:120px;line-height:1.02">{t}</div>
      <div class="rule"></div>
      <div class="card"><p style="font-size:36px">{d["body"]}</p></div>
      <div style="margin-top:56px"><span class="cta" style="font-size:30px;padding:30px 52px">{d["cta"]} →</span></div>
    </div>
    <div class="foot" style="height:110px">{SITE}<i>•</i>{TEL}</div></div>''', h=1920)


# ---------- Görünüm temaları (Brand Kit paleti içinde zemin seçenekleri) ----------
NO_THEME = {"uzman", "alinti", "soru_bant", "pasaport_kapak", "pasaport_ic", "pasaport_son"}   # uzman / blog serisi kendi sabit düzenini korur
THEMES = {
  "krem": {"name": "Krem zemin", "css": """
.post.th-krem{background:var(--c)!important;color:var(--k)!important}
.th-krem .h{color:var(--k)!important}
.th-krem .glass{background:#fff!important;box-shadow:inset 0 0 0 3px #EEDFCB!important}.th-krem .glass p{color:var(--k)!important}.th-krem .glass b{color:var(--b)!important}
.th-krem .dots i{background:rgba(0,0,0,.18)}"""},
  "koyu": {"name": "Koyu (kömür) zemin", "css": """
.post.th-koyu{background:var(--ch)!important;color:#fff!important}
.th-koyu .h{color:#fff!important}.th-koyu .h .b{color:var(--pe)!important}
.th-koyu .card,.th-koyu .nb,.th-koyu .fact{background:var(--cc)!important;box-shadow:inset 0 0 0 3px rgba(255,255,255,.16)!important;color:#fff!important}
.th-koyu .card b{color:var(--o)!important}.th-koyu .fact small{color:var(--pe)!important}
.th-koyu .circ{opacity:.10}.th-koyu .vs{background:var(--ch)!important}
.th-koyu .cta.ol{background:transparent!important;color:#fff!important}
.th-koyu .swipe{color:var(--o)!important}.th-koyu [style*="color:var(--s)"]{color:var(--pe)!important}
.th-koyu [style*="background:var(--ch)"]{box-shadow:inset 0 0 0 3px rgba(255,255,255,.2)}
.th-koyu .dots i{background:rgba(255,255,255,.25)}"""},
  "bordo": {"name": "Bordo zemin", "css": """
.post.th-bordo{background:var(--bd)!important;color:#fff!important}
.th-bordo .h{color:#fff!important}.th-bordo .h .b{color:var(--pe)!important}
.th-bordo .card,.th-bordo .nb,.th-bordo .fact,.th-bordo .glass{background:#fff!important;box-shadow:none!important;color:var(--k)!important}
.th-bordo .glass p{color:var(--k)!important}.th-bordo .card b,.th-bordo .glass b{color:var(--b)!important}
.th-bordo .myth,.th-bordo .quote{background:var(--ch)!important}.th-bordo .tag:not(.s):not(.o):not(.k){background:var(--ch)!important}
.th-bordo .circ{opacity:.10}.th-bordo .vs{background:var(--bd)!important}
.th-bordo .cta.ol{background:transparent!important;color:#fff!important;box-shadow:inset 0 0 0 4px #fff!important}
.th-bordo .swipe{color:var(--pe)!important}.th-bordo .rule.b{background:var(--pe)!important}
.th-bordo [style*="color:var(--s)"]{color:var(--pe)!important}
.th-bordo .dots i{background:rgba(255,255,255,.3)}"""},
}


# ---------- Yeni kompozisyon aileleri ----------
PHOTO_SLOT = {"soru_bant", "alinti"}   # fotoğraf yüklenirse bu şablonlarda fotoğraf alanı kullanılır

def _visual(photo, h, art):
    """Fotoğraf alanı: fotoğraf varsa kaplar; yoksa markanın grafik düzeni (boş alan bırakmaz)."""
    if photo:
        return f'<img src="{photo}" style="position:absolute;inset:0;width:100%;height:{h}px;object-fit:cover">'
    return art

def soru_bant(d):
    """Seri: Soru Bandı — üstte görsel alan, ortada turuncu soru bandı, altta koyu kaydırma bandı (Instagram carousel kapağı dili).
    d: tag, q[list 2-3], sub, cta, photo(isteğe bağlı)"""
    art = (f'<div style="position:absolute;left:0;right:0;top:0;height:700px;background:var(--c);overflow:hidden">'
           f'{circ(560,-220,640,"#F8D6A8")}{circ(-160,360,420,"#FFE8CD")}{circ(760,420,240,"#DCE6DF")}'
           f'{flower(300,90,250,"#F48011",4,.9)}{flower(120,330,120,"#A6264C",3,.6)}{flower(780,120,90,"#577D66",3,.7)}</div>')
    q = "<br>".join(d["q"])
    return post(f'''{_visual(d.get("photo"), 700, art)}{tile()}
    <div class="top" style="top:72px"><span class="tag">{d["tag"]}</span></div>
    <div style="position:absolute;left:0;right:0;top:640px;bottom:96px;display:flex;flex-direction:column">
      <div style="background:var(--o);padding:52px 64px 56px"><div class="h" style="font-size:78px;color:#fff;line-height:1.04">{q}</div></div>
      <div style="flex:1;background:var(--ch);padding:40px 64px;display:flex;align-items:center;justify-content:space-between;gap:40px">
        <p style="font:600 30px/1.38 Montserrat;color:#fff;max-width:620px">{d["sub"]}</p>
        <span class="cta" style="flex:none">{d["cta"]} →</span></div></div>
    {foot()}''')

def alinti(d):
    """Seri: Alıntı Kartı — ortalanmış kart, büyük tırnak, iki renkli cümle, imza (Instagram alıntı postu dili).
    d: q1, q2, line, photo(isteğe bağlı). İmza her zaman kurum adıdır; gerçek kişiye söz atfedilmez."""
    art = (f'<div style="position:absolute;inset:0;background:linear-gradient(160deg,#FFE8CD 0%,#F8D6A8 45%,#DCE6DF 100%)"></div>'
           f'{flower(-160,-120,360,"#FFFFFF",3,.7)}{flower(760,960,260,"#FFFFFF",3,.7)}{circ(780,-140,380,"rgba(255,255,255,.35)")}')
    return post(f'''{_visual(d.get("photo"), 1350, art)}{tile()}
    <div style="position:absolute;left:110px;right:110px;top:250px;bottom:190px;border-radius:48px;background:rgba(255,255,255,.93);
      box-shadow:0 30px 80px rgba(0,0,0,.12);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:60px 70px">
      <div style="font:800 170px/.55 'Playfair Display';color:var(--o);height:80px">“</div>
      <div class="h" style="font-size:60px;line-height:1.12;margin-top:30px">{d["q1"]}<br><span class="b">{d["q2"]}</span></div>
      <div style="width:160px;height:6px;border-radius:3px;background:var(--s);margin:40px 0 34px"></div>
      <p style="font:600 32px/1.4 Montserrat;color:var(--k);max-width:640px">{d["line"]}</p>
      <div style="font:800 24px/1 Montserrat;letter-spacing:.14em;color:var(--o);margin-top:38px">— ABA PSİKOLOJİ</div>
    </div>{foot()}''')


# ---------- Kütüphane: yeni kompozisyon aileleri ve Story ----------
_LIB0 = library
def library():
    return _LIB0() + [
      ("07-soru-bandi", soru_bant(dict(tag="Okulun ilk haftaları", q=["Dikkati mi dağınık,", "yöntemi mi yanlış?"],
        sub="Odaklanamamak çoğu zaman irade değil, yöntem meselesidir.", cta="Kaydır"))),
      ("08-alinti-karti", alinti(dict(q1="Kaygı, yolun kapandığını değil;", q2="bu yolun senin için önemli olduğunu söyler.",
        line="Nefes al ve yalnızca bir sonraki adımına dön."))),
      ("09-story", story(dict(tag="Sınav haftası", title=["Uykusuz", "gece", "işe", "yaramaz."],
        body="Son gece yeni konu değil, <b>dinlenmiş bir zihin</b> kazandırır. Bu akşam erken kapat.", cta="Birlikte planlayalım"))),
    ]

META["intro"] = ("Sekiz Feed serisi ve bir Story düzeni. Her seri farklı bir kompozisyon ailesidir: koyu kart, soru kutusu, "
                 "kaydırmalı karşılaştırma, illüstrasyonlu durak, adım listesi, uzman notu, renk bantları ve ortalanmış alıntı. "
                 "Turuncu iletişim bandı ve sağ üstteki logo karosu her postta sabittir.")
META["series"] += [
  dict(id="07", name="Soru Bandı", img=["07-soru-bandi"], when="Öğrencinin ya da velinin aklındaki tek soruyu büyük bir bantla sormak; fotoğraflı ya da fotoğrafsız.",
       freq="2 haftada 1", fmt="Tek post · renk bantları",
       slots=["Üst alan: fotoğraf (yüklenirse) ya da çiçek ve daire illüstrasyonu", "Turuncu bant: iki satırlık büyük soru", "Koyu bant: kısa cevap ipucu + CTA hapı", "Fotoğraf yoksa alan boş kalmaz"],
       caption="Okulun ilk haftalarında odaklanamıyor musun? 🍂\n\nÇoğu zaman sorun irade değil, yöntem. Kaydır, küçük bir yöntem değişikliğiyle başlayalım.\n\nABA Psikoloji ile odak planını birlikte kuralım.\n#ABAPsikoloji #Odaklanma #ÖğrenciPsikolojisi #YeniDönem"),
  dict(id="08", name="Alıntı Kartı", img=["08-alinti-karti"], when="Kaygıyı normalleştiren kısa, sakin bir cümle; hafta ortası nefes postu.",
       freq="Haftada 1 · Çarşamba", fmt="Tek post · ortalanmış kart",
       slots=["Zemin: fotoğraf (yüklenirse) ya da şeftali–adaçayı geçişi", "Ortalanmış beyaz kart, turuncu tırnak", "İki renkli cümle: mürekkep + bordo", "İmza her zaman “ABA Psikoloji”; kişiye söz atfedilmez"],
       caption="Kaygı bazen ne kadar önemsediğinin işaretidir. 🌿\n\nHer şeyi bugün çözmek zorunda değilsin. Yalnızca bir sonraki adımına dön.\n\nABA Psikoloji ile birlikte.\n#ABAPsikoloji #SınavKaygısı #Mindfulness #Nefes"),
  dict(id="09", name="Instagram Story", img=["09-story"], when="Feed postunu destekleyen tek ekranlık hatırlatma; 1080×1920.",
       freq="Feed postlarıyla birlikte", fmt="Story · 9:16",
       slots=["Üst ve alt güvenli alan boş", "Üç renkli başlık, son satır turuncu", "Beyaz kart + CTA", "Turuncu iletişim bandı"],
       caption="Story'de caption görünmez; öne çıkanlara eklenirken kısa not: “Sınav haftası hatırlatması.” #ABAPsikoloji"),
]
