"""ABA Eğitim post şablonları (1080×1350)."""
from engine import doc, asset
LOGO = asset("aba-egitim/logo-mark-white.png")
SITE, TEL, MAIL = "abaegitim.com", "+90 212 287 86 06", "info@abaegitim.com"

CSS = """
:root{--o:#F95B1C;--oc:#E45823;--n:#06162F;--nd:#040D1E;--nb:#0B2345;--cr:#F8F0E3;--pa:#F7F1E5;--r:#7E060F;--rd:#4A0309;--bo:#620510;--g:#C97304}
.post{font-family:Montserrat;color:#fff;background:var(--nd)}
.deco{position:absolute;pointer-events:none}
.tile{position:absolute;right:64px;top:64px;width:112px;height:112px;border-radius:24px;background:var(--o);display:grid;place-items:center}.tile img{width:68px}
.tag{display:inline-block;padding:13px 28px;border-radius:99px;background:var(--o);color:#fff;font:800 22px/1 Montserrat;letter-spacing:.08em;text-transform:uppercase}
.tag.cr{background:var(--cr);color:var(--n)}
.top{position:absolute;left:64px;top:96px}
.foot{position:absolute;left:0;right:0;bottom:0;height:96px;background:var(--n);border-top:4px solid var(--o);display:flex;justify-content:center;align-items:center;gap:34px;font:600 23px/1 Montserrat;color:#fff}
.foot span{display:flex;align-items:center;gap:12px}.foot svg{width:26px;height:26px}
.h{font:900 90px/1.0 Montserrat;text-transform:uppercase;letter-spacing:-.015em}.h em{font-style:normal;color:var(--o)}
.osw{font-family:Oswald;font-weight:700;text-transform:uppercase;letter-spacing:.005em}
.pop{font-family:Poppins}
.cta{display:inline-flex;align-items:center;gap:12px;padding:24px 40px;border-radius:99px;background:var(--o);color:#fff;font:800 24px/1 Montserrat;letter-spacing:.04em;text-transform:uppercase}
.cta.cr{background:var(--cr);color:var(--n)}.cta.ol{background:none;box-shadow:inset 0 0 0 3px #fff;color:#fff}
.cream{border-radius:28px;background:var(--cr);color:var(--n);padding:36px 44px}
.nrow{display:flex;gap:0;border-radius:24px;overflow:hidden;box-shadow:inset 0 0 0 3px var(--o)}
.nrow .num{flex:none;width:170px;background:var(--o);display:grid;place-items:center;font:900 64px/1 Montserrat}
.nrow .tx{flex:1;background:var(--n);padding:44px 40px}.nrow h3{font:800 40px/1.15 Montserrat;text-transform:uppercase}.nrow p{font:500 31px/1.42 Montserrat;opacity:.9;margin-top:16px}
.dots{position:absolute;bottom:126px;left:0;right:0;display:flex;justify-content:center;gap:12px}.dots i{width:12px;height:12px;border-radius:50%;background:rgba(255,255,255,.3)}.dots i.on{background:var(--o);width:34px;border-radius:6px}
.page{position:absolute;right:200px;top:104px;font:800 26px/1 Montserrat;color:var(--o)}
.glow{position:absolute;border-radius:50%;filter:blur(90px);opacity:.55}
.feat{display:grid;gap:20px}.feat div{display:flex;gap:20px;align-items:center;font:600 32px/1.3 Montserrat}.feat div::before{content:"";flex:none;width:22px;height:22px;background:var(--o);border-radius:4px}
.stat{border-radius:28px;background:var(--n);box-shadow:inset 0 0 0 3px rgba(249,91,28,.6);padding:34px 32px}
.stat b{display:block;font:800 104px/1 Poppins;color:var(--o)}.stat span{display:block;font:500 26px/1.35 Poppins;margin-top:10px}
"""
ICON = {
 "web": '<svg viewBox="0 0 24 24" fill="none" stroke="#F95B1C" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/></svg>',
 "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="#F95B1C" stroke-width="2"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="#F95B1C" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'}

def tile(): return f'<div class="tile"><img src="{LOGO}"></div>'
def foot(): return f'<div class="foot"><span>{ICON["web"]}{SITE}</span><span>{ICON["tel"]}{TEL}</span><span>{ICON["mail"]}{MAIL}</span></div>'
def dots(n, i): return '<div class="dots">' + "".join(f'<i class="{"on" if k==i else ""}"></i>' for k in range(n)) + "</div>"
def glow(x, y, d, c): return f'<div class="deco glow" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;background:{c}"></div>'
def arcs(x, y, c="#F95B1C", op=.35):
    return f'<svg class="deco" style="left:{x}px;top:{y}px;opacity:{op}" width="520" height="520">' + "".join(f'<circle cx="260" cy="260" r="{r}" fill="none" stroke="{c}" stroke-width="2"/>' for r in (120, 180, 240)) + "</svg>"
def post(inner, bg=""): return doc(CSS, f'<div class="post" style="{bg}">{inner}</div>')

def kabul(d):
    return post(f'''{glow(560,-160,620,"#F95B1C")}{glow(-260,820,520,"#0B2345")}{tile()}
    <div class="top"><span class="tag">{d["tag"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;top:250px">
      <div class="pop" style="font-weight:800;font-size:330px;line-height:.9;color:var(--o);letter-spacing:-.04em">{d["num"]}</div>
      <div class="pop" style="font-weight:700;font-size:62px;line-height:1.1;margin-top:10px">{d["line1"]} <i style="font-weight:300">{d["italic"]}</i><br>{d["line2"]}</div>
      {f'<div style="margin:46px -64px 0;background:var(--pa);color:var(--n);padding:30px 64px;font:800 32px/1 Montserrat;letter-spacing:.06em;display:flex;justify-content:space-between">{"".join(f"<span>{s}</span>" for s in d["schools"])}</div>' if d.get("schools") else '<div style="width:200px;height:8px;background:var(--o);border-radius:4px;margin-top:46px"></div>'}
      <p style="font:500 32px/1.45 Montserrat;margin:44px 0 40px;max-width:860px">{d["body"]}</p>
      <span class="cta">{d["cta"]} →</span>
    </div>{foot()}''')

def son_tarih(d):
    ck = "".join(f'<div style="display:flex;gap:18px;align-items:center;font:600 30px/1.3 Montserrat"><span style="flex:none;width:36px;height:36px;border-radius:8px;box-shadow:inset 0 0 0 3px var(--o)"></span>{x}</div>' for x in d["checks"])
    return post(f'''{arcs(620,-140)}{glow(-200,-200,520,"#0B2345")}{tile()}
    <div class="top"><span class="tag">Son tarih</span></div>
    <div style="position:absolute;left:64px;right:64px;top:250px">
      <div style="font:900 196px/.9 Montserrat;color:var(--o);letter-spacing:-.04em">{d["day"]}</div>
      <div style="font:900 96px/1 Montserrat;margin-top:8px">{d["year"]}</div>
      <div style="font:800 34px/1.25 Montserrat;margin-top:30px;text-transform:uppercase">{d["what"]}</div>
      <div class="cream" style="margin-top:40px;display:grid;gap:22px"><div style="font:800 24px/1 Montserrat;letter-spacing:.1em;color:var(--oc)">KONTROL LİSTESİ</div>{ck}</div>
      <div style="margin-top:36px"><span class="cta">{d["cta"]}</span></div>
      <p style="font:500 21px/1.4 Montserrat;opacity:.7;margin-top:22px">{d["note"]}</p>
    </div>{foot()}''')

def sinav(d):
    ft = "".join(f"<div>{x}</div>" for x in d["feat"])
    return post(f'''{glow(600,-200,600,"#F95B1C")}{tile()}
    <div class="top"><span class="tag cr">Hazırlık programı</span></div>
    <div style="position:absolute;left:64px;right:64px;top:240px">
      <div class="osw" style="font-size:200px;line-height:.9" lang="en">{d["exam1"]}<br><span style="color:var(--o)">{d["exam2"]}</span></div>
      <div style="font:800 40px/1.2 Montserrat;margin:26px 0 22px;text-transform:uppercase">{d["sub"]}</div>
      {('<span style="display:inline-block;padding:16px 26px;border-radius:99px;box-shadow:inset 0 0 0 3px var(--cr);font:800 26px/1 Montserrat">'+d["pill"]+'</span>') if d.get("pill") else ""}
      <div class="feat" style="margin:40px 0 46px">{ft}</div>
      <div style="display:flex;gap:18px"><span class="cta ol">{d.get("cta2","Sınırlı kontenjan")}</span><span class="cta">{d["cta"]}</span></div>
    </div>{foot()}''', "background:linear-gradient(160deg,#7E060F 0%,#4A0309 100%)")

def keske_kapak(d):
    return post(f'''{glow(520,-120,640,"#F95B1C")}{arcs(-180,860,"#F7F1E5",.25)}{tile()}
    <div class="top"><span class="tag">{d["tag"]}</span></div><div class="page">1/{d["n"]}</div>
    <div style="position:absolute;left:64px;right:64px;top:300px">
      <div class="h" style="font-size:96px">{d["h"]}</div>
      <p style="font:600 34px/1.4 Montserrat;margin:40px 0;max-width:820px;opacity:.92">{d["body"]}</p>
      <span class="cta cr">{d.get("cta","Kaydet • sonra dön")}</span>
    </div>{dots(d["n"],0)}{foot()}''')

def keske_sayfa(d):
    rows = "".join(f'<div class="nrow"><div class="num">{n}</div><div class="tx"><h3>{h}</h3><p>{p}</p></div></div>' for n, h, p in d["rows"])
    return post(f'''{glow(700,900,520,"#0B2345")}{tile()}
    <div class="top"><span class="tag">{d["tag"]}</span></div><div class="page">{d["i"]+1}/{d["n"]}</div>
    <div style="position:absolute;left:64px;right:64px;top:240px">
      <div class="h" style="font-size:86px;margin-bottom:54px">{d["h"]}</div>
      <div style="display:grid;gap:40px">{rows}</div>
      <div style="margin-top:40px"><span class="cta cr" style="font-size:22px">{d["sum"]}</span></div>
    </div>{dots(d["n"],d["i"])}{foot()}''')

def keske_son(d):
    return post(f'''{glow(-200,-160,620,"#F95B1C")}{arcs(640,820,"#F7F1E5",.25)}{tile()}
    <div class="page" style="top:104px">{d["n"]}/{d["n"]}</div>
    <div style="position:absolute;left:64px;right:64px;top:300px">
      <div class="h" style="font-size:112px">“Keşke” değil,<br><em>“iyi ki.”</em></div>
      <p style="font:600 34px/1.4 Montserrat;margin:40px 0 50px;max-width:820px">{d["body"]}</p>
      <div style="display:grid;gap:18px;justify-items:start">{"".join(f'<span class="cta {c}">{t}</span>' for c, t in zip(["", "cr", "ol"], d.get("ctas", ["Sınırlı kontenjan", "Bizimle iletişime geç", "Takipte kal"])))}</div>
    </div>{dots(d["n"],d["n"]-1)}{foot()}''')

def veri(d):
    st = "".join(f'<div class="stat"><b>{a}</b><span>{b}</span></div>' for a, b in d["stats"])
    return post(f'''{glow(560,-200,600,"#F95B1C")}{tile()}
    <div class="top"><span class="tag">{d["tag"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;top:250px">
      <div class="pop" style="font-weight:800;font-size:120px;line-height:.95">{d["title"]}</div>
      <div class="pop" style="font-weight:300;font-style:italic;font-size:46px;margin:18px 0 50px;color:var(--cr)">{d["sub"]}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:22px">{st}</div>
      <p style="font:500 30px/1.45 Montserrat;margin:44px 0 36px">{d["body"]}</p>
      <span class="cta">{d["cta"]}</span>
      <p style="font:500 21px/1 Montserrat;opacity:.6;margin-top:26px">{d["src"]}</p>
    </div>{foot()}''')

def building():
    cols = "".join(f'<rect x="{60+i*56}" y="250" width="22" height="190" fill="none" stroke="#C97304" stroke-width="3"/>' for i in range(7))
    return f'''<svg class="deco" style="right:70px;top:250px" width="520" height="520" viewBox="0 0 520 520">
    <path d="M40 250 L260 120 L480 250 Z" fill="none" stroke="#C97304" stroke-width="3"/><path d="M200 120 Q260 20 320 120" fill="none" stroke="#C97304" stroke-width="3"/>
    <line x1="260" y1="20" x2="260" y2="0" stroke="#C97304" stroke-width="3"/>{cols}<rect x="30" y="440" width="460" height="22" fill="none" stroke="#C97304" stroke-width="3"/>
    <rect x="10" y="462" width="500" height="22" fill="none" stroke="#C97304" stroke-width="3"/></svg>'''

def uzman(d):
    return post(f'''{building()}{tile()}
    <div class="top"><span class="tag cr">{d["tag"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;top:260px">
      <div style="font:600 24px/1 Montserrat;letter-spacing:.16em;color:var(--g)">{d["meta"]}</div>
    </div>
    <div style="position:absolute;left:64px;right:64px;top:720px">
      <div class="osw" style="font-size:118px;line-height:.95">{d["h1"]}<br><span style="color:var(--o)">{d["h2"]}</span></div>
      <p style="font:500 32px/1.42 Montserrat;margin:30px 0 34px;max-width:840px">{d["body"]}</p>
      <div style="font:800 28px/1 Montserrat;color:var(--g)">{d.get("cta","Blog yazımızı inceleyiniz →")}</div>
    </div>{foot()}''', "background:linear-gradient(180deg,#620510 0%,#3D030A 100%)")

def library():
    n = 4
    return [
      ("01-kabul-duyurusu", kabul(dict(tag="Kabul sonuçları", num="221", line1="öğrencimiz", italic="o e-postayı", line2="aldı.",
        schools=["OXFORD", "CAMBRIDGE", "IMPERIAL", "LSE", "UCL"], body="Tesadüf değil, plan. Üç yıllık bir yöntem, tek bir danışmanlık odası.", cta="Yoruma hedef okulunu yaz"))),
      ("02-son-tarih", son_tarih(dict(day="1 KASIM", year="2026", what="ABD erken başvuru<br><span lang='en'>Early Decision · Early Action</span>",
        checks=["Common App hesabın hazır mı?", "Ana essay son okumada mı?", "Tavsiye mektupları istendi mi?"],
        cta="DM “TAKVİM” yaz • yol haritanı al", note="Tarihler okula göre değişebilir; hedef okulunun sitesinden doğrula."))),
      ("03-sinav-programi", sinav(dict(exam1="Digital", exam2="SAT", sub="Doğru stratejiyle hazırlan.", pill="2 BÖLÜM • 400–1600 PUAN",
        feat=["Diagnostik deneme ile başlangıç", "Kişisel çalışma planı", "Modül bazlı ders ve tekrar", "Düzenli deneme ve analiz"], cta="Planını bizle oluştur"))),
      ("04-keske-1-kapak", keske_kapak(dict(n=n, tag="ABD başvurusu", h="ABD başvurusunda<br><em>“keşke”</em> dedirten<br>4 şey", body="Common App sezonu başladı. Bu dört detayı şimdiden bil."))),
      ("04-keske-2", keske_sayfa(dict(n=n, i=1, tag="İlk 2 kural", h="İlk 2<br><em>şaşırtan kural</em>", sum="Ana fikir = essay'in omurgası",
        rows=[("01", "Ana essay 650 kelimeyle sınırlı", "Her cümle bir karar. Hikâyeni tek bir ana fikre indir."),
              ("02", "Tavsiye mektubu erken istenir", "Öğretmenine en az 4–6 hafta önceden haber ver.")]))),
      ("04-keske-3", keske_sayfa(dict(n=n, i=2, tag="Son 2 detay", h="Son 2<br><em>kritik detay</em>", sum="Derinlik > sayı",
        rows=[("03", "Aktivite listesinde 10 satır var", "Sayı değil derinlik: en güçlü 3 aktiviteni öne al."),
              ("04", "“<span lang='en'>Test-optional</span>” sınavsız demek değil", "Güçlü bir puan dosyanı hâlâ güçlendirir; okul politikasını tek tek kontrol et.")]))),
      ("04-keske-4-kapanis", keske_son(dict(n=n, body="Hedefin büyük mü? Planın da büyük olsun. Başvuru takvimini birlikte kuralım."))),
      ("05-veri-karti", veri(dict(tag="Sayılarla", title="IB Diploma", sub="üç sayıda bir program",
        stats=[("45", "en yüksek toplam puan"), ("24", "diploma için en düşük puan"), ("3", "çekirdek: TOK · EE · CAS")],
        body="Hedef okulunun istediği puanı bil; planını o sayıdan geriye doğru kur.", cta="DM “IB” yaz • ücretsiz rehberlik", src="Kaynak: ibo.org"))),
      ("06-uzman-serisi", uzman(dict(tag="Uzman serisi", meta="BLOG · 6 DK OKUMA", h1="Yüksek puan", h2="yetmez.",
        body="Başvuru dosyası bir hikâye anlatır. Puan kapıyı aralar; seni içeri alan, o hikâyedir."))),
    ]

META = dict(
  brand="aba_egitim", lang="tr",
  intro="Altı seri: kanıt, takvim, sınav, ipucu, veri ve uzman. Her post tek bir sayı, tarih ya da okul adıyla açılır ve tek bir anahtar kelimeli eyleme bağlanır.",
  constants=["Sağ üstte turuncu logo karosu, altta lacivert ikonlu iletişim bandı", "Tek turuncu (#F95B1C) + gece laciverti; kırmızı yalnızca sınav serisi, bordo yalnızca uzman serisi", "Üç başlık fontu: Montserrat (ana), Oswald (sınav/uzman), Poppins (kabul/veri)", "Site adresi her zaman “abaegitim.com”"],
  series=[
    dict(id="01", name="Kabul Duyurusu", img=["01-kabul-duyurusu"], when="Gerçek kabul sonuçlarını sayı ve okul adlarıyla duyurmak için.", freq="Sonuç dönemlerinde · ayda 1–2", fmt="Tek post · Poppins",
      slots=["Dev sayı (yalnızca doğrulanmış sonuç)", "Poppins cümle + light italik vurgu", "Krem okul bandı (en fazla 5 okul)", "Yöntem cümlesi + yorum çağrısı"],
      caption="Bu yıl 221 öğrencimiz Oxford, Cambridge, Imperial, LSE ve UCL'den kabul aldı. 🎓\n\nTesadüf değil, plan: üç yıllık bir yöntem, tek bir danışmanlık odası.\n\nSenin hedef okulun hangisi? Yoruma yaz.\n#abaegitim #yurtdışıeğitim #profdrgamzesart #G5Universities"),
    dict(id="02", name="Son Tarih", img=["02-son-tarih"], when="Kritik bir başvuru tarihini kontrol listesiyle hatırlatmak için.", freq="Tarihten 2–3 hafta önce", fmt="Tek post · lacivert",
      slots=["Dev tarih (turuncu) + yıl", "Ne için olduğu: program / başvuru türü", "Krem kontrol listesi (3 madde)", "DM anahtar kelimesi + doğrulama notu"],
      caption="1 Kasım 2026: ABD'de erken başvuru (Early Decision / Early Action) için en yaygın tarih. ⏳\n\nCommon App hesabın, ana essay'in ve tavsiye mektupların hazır mı?\n\nDM'e “TAKVİM” yaz, yol haritanı gönderelim. 📩\n#abaegitim #ABDÜniversite #CommonApp #EarlyDecision"),
    dict(id="03", name="Sınav Programı", img=["03-sinav-programi"], when="Bir sınav hazırlık programını duyurmak için.", freq="Dönem başlarında", fmt="Tek post · sınav kırmızısı",
      slots=["Oswald dev sınav adı (ikinci satır turuncu)", "Sınavın doğrulanmış biçimi (bölüm, puan aralığı)", "4 madde: programın adımları", "Kontur “Sınırlı kontenjan” + turuncu CTA"],
      caption="Digital SAT: 2 bölüm, 400–1600 puan. Doğru stratejiyle hazırlan. 📊\n\nDiagnostik denemeyle başlıyor, sana özel planla ilerliyoruz.\n\nKontenjan sınırlı: DM'e “SAT” yaz.\n#abaegitim #DigitalSAT #SATHazırlık #yurtdışıeğitim"),
    dict(id="04", name="“Keşke” Listesi", img=["04-keske-1-kapak", "04-keske-2", "04-keske-3", "04-keske-4-kapanis"], when="Öğrencilerin sonradan “keşke” dediği detayları kaydırmalı listeyle anlatmak için.", freq="2 haftada 1", fmt="Carousel · 4 sayfa",
      slots=["Kapak: sayı + “keşke” + “Kaydet • sonra dön”", "Sayfa 2–3: turuncu numara blokları 01–04", "Her sayfada krem özet hapı", "Kapanış: “Keşke değil, iyi ki.” + 3 buton"],
      caption="ABD başvurusunda öğrencilerin “keşke” dediği 4 şey. 🎯\n\n1️⃣ Ana essay 650 kelimeyle sınırlı  2️⃣ Tavsiye mektubu erken istenir  3️⃣ Aktivite listesinde 10 satır var  4️⃣ Test-optional sınavsız demek değil\n\nKaydet, başvuru döneminde geri dön. 📌\n#abaegitim #CommonApp #ABDÜniversite #ÜniversiteBaşvurusu"),
    dict(id="05", name="Sayılarla", img=["05-veri-karti"], when="Bir programı ya da sınavı üç doğrulanmış sayıyla anlatmak için.", freq="Ayda 2", fmt="Tek post · Poppins",
      slots=["Program adı + light italik alt başlık", "3 sayı kutusu (kaynaklı)", "Planlama cümlesi", "DM anahtar kelimesi + kaynak satırı"],
      caption="IB Diploma üç sayıda: 45 en yüksek puan, 24 diploma için en düşük puan, 3 çekirdek (TOK, EE, CAS). 📊\n\nHedef okulunun istediği puanı bil, planını o sayıdan geriye doğru kur.\n\nDM'e “IB” yaz.\n#abaegitim #IBDiploma #ÜniversiteBaşvurusu"),
    dict(id="06", name="Uzman Serisi", img=["06-uzman-serisi"], when="Blog yazılarını akademik otoriteyle duyurmak için.", freq="Ayda 2", fmt="Tek post · uzman bordosu",
      slots=["Etiket + okuma süresi (altın)", "Çizgisel bina illüstrasyonu", "Oswald başlık; ikinci satır turuncu", "Tek cümle özet + blog linki"],
      caption="Yüksek puan yetmez. ✍️\n\nPuan kapıyı aralar; seni içeri alan, dosyanın anlattığı hikâyedir. Yeni blog yazımız biyografideki linkte.\n#abaegitim #profdrgamzesart #ÜniversiteBaşvurusu #Blog"),
  ],
  calendar=[("Pzt","Son Tarih","1 Kasım erken başvuru"),("Sal","Sayılarla","IB Diploma"),("Çar","“Keşke” Listesi","ABD başvurusu"),("Per","Sınav Programı","Digital SAT"),("Cum","Reels","Öğrenci yorumu"),
            ("Pzt","Uzman Serisi","Yüksek puan yetmez"),("Sal","Son Tarih","UCAS takvimi"),("Çar","Kabul Duyurusu","Erken kabul sonuçları"),("Per","“Keşke” Listesi","UCAS personal statement"),("Cum","Etkileşim","Kelime avı oyunu")],
  hooks=["Bu yıl … öğrencimiz …'dan kabul aldı.", "… tarihi: kaçırma!", "Ortak noktası şans değil — bir strateji.", "… öğrencilerinin “keşke” dediği … şey", "… üç sayıda:", "Notunu şansa bırakma.", "Hedefin büyük mü? Planın da büyük olsun.", "Tesadüf değil, plan.", "Tek bir oda. Üç yıllık bir yöntem.", "Son 3 gün!"],
  ctas=["DM “…” yaz • yol haritanı al", "Yoruma hedef okulunu yaz", "Planını bizle oluştur", "Sınırlı kontenjan", "Kaydet • sonra dön", "Blog yazımızı inceleyiniz →"],
)


# ---------- Instagram Story (1080×1920) ----------
def story(d):
    """Story: gece laciverti, turuncu ışık, son satırı turuncu blok başlık. d: tag, title[list], body(html), cta"""
    lines = d["title"]; n = len(lines)
    t = "".join(f'<em style="display:block;white-space:nowrap">{x}</em>' if k == n - 1 else f'<span style="display:block;white-space:nowrap">{x}</span>' for k, x in enumerate(lines))
    return doc(CSS, f'''<div class="post">{glow(520,-120,760,"#F95B1C")}{glow(-300,1300,640,"#0B2345")}{arcs(640,1200)}
    <div class="tile" style="top:220px">{f'<img src="{LOGO}">'}</div>
    <div style="position:absolute;left:72px;top:250px"><span class="tag">{d["tag"]}</span></div>
    <div style="position:absolute;left:72px;right:72px;top:380px;bottom:300px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start">
      <div class="h" style="font-size:112px;line-height:1.0">{t}</div>
      <div style="width:200px;height:8px;background:var(--o);border-radius:4px;margin:44px 0"></div>
      <p style="font:500 38px/1.45 Montserrat;max-width:900px">{d["body"]}</p>
      <div style="margin-top:60px"><span class="cta" style="font-size:30px;padding:30px 50px">{d["cta"]} →</span></div>
    </div>
    <div class="foot" style="height:110px"><span>{ICON["web"]}{SITE}</span><span>{ICON["tel"]}{TEL}</span></div></div>''', h=1920)


# ---------- Görünüm temaları (Brand Kit paleti içinde zemin seçenekleri) ----------
NO_THEME = {"uzman", "foto_duyuru"}   # uzman / blog serisi kendi sabit düzenini korur
THEMES = {
  "lacivert": {"name": "Gece laciverti", "css": """
.post.th-lacivert{background:var(--nd)!important}"""},
  "kirmizi": {"name": "Sınav kırmızısı", "css": """
.post.th-kirmizi{background:linear-gradient(160deg,#7E060F 0%,#4A0309 100%)!important}
.th-kirmizi .glow{opacity:.35}"""},
  "krem": {"name": "Krem zemin", "css": """
.post.th-krem{background:var(--cr)!important;color:var(--n)!important}
.th-krem .glow{opacity:.16}.th-krem .nrow .tx,.th-krem .stat{color:#fff}
.th-krem .cream{background:#fff!important;box-shadow:inset 0 0 0 3px rgba(6,22,47,.12)}
.th-krem .cta.cr,.th-krem .tag.cr{background:var(--n)!important;color:#fff!important}
.th-krem .cta.ol{box-shadow:inset 0 0 0 3px var(--n)!important;color:var(--n)!important}
.th-krem [style*="background:var(--pa)"]{background:var(--n)!important;color:#fff!important}
.th-krem [style*="color:var(--cr)"]{color:var(--oc)!important}
.th-krem .dots i{background:rgba(6,22,47,.25)}"""},
}


# ---------- Yeni kompozisyon aileleri ----------
PHOTO_SLOT = {"foto_duyuru"}

def campus():
    """Fotoğraf yokken kullanılan çizgisel kampüs silüeti (gotik kemerler, kule)."""
    arches = "".join(f'<path d="M{40+i*120} 760 V560 Q{100+i*120} 470 {160+i*120} 560 V760" fill="none" stroke="#F95B1C" stroke-width="3" opacity=".55"/>' for i in range(8))
    return (f'<svg class="deco" style="left:0;top:90px" width="1080" height="800" viewBox="0 0 1080 800">'
            f'<path d="M470 470 V180 L540 60 L610 180 V470" fill="none" stroke="#F95B1C" stroke-width="4"/>'
            f'<path d="M510 470 V250 Q540 210 570 250 V470" fill="none" stroke="#F95B1C" stroke-width="3"/>'
            f'<line x1="540" y1="60" x2="540" y2="10" stroke="#F95B1C" stroke-width="3"/>{arches}'
            f'<line x1="0" y1="760" x2="1080" y2="760" stroke="#F7F1E5" stroke-width="2" opacity=".4"/></svg>')

def foto_duyuru(d):
    """Seri: Fotoğraflı Duyuru — tam sayfa fotoğraf (yoksa kampüs çizimi), alttan koyu geçiş, dev üç satırlık başlık.
    d: kicker, h1, h2, h3, sub, photo(isteğe bağlı)"""
    vis = (f'<img src="{d["photo"]}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">' if d.get("photo")
           else f'{glow(380,60,620,"#F95B1C")}{campus()}')
    return post(f'''{vis}<div class="deco" style="inset:0;background:linear-gradient(180deg,rgba(4,13,30,0) 40%,rgba(4,13,30,.94) 72%)"></div>{tile()}
    <div class="top"><span class="tag">{d["kicker"]}</span></div>
    <div style="position:absolute;left:64px;right:64px;bottom:150px">
      <div class="h" style="font-size:118px;line-height:.98">{d["h1"]}<br><em>{d["h2"]}</em><br>{d["h3"]}</div>
      <div style="display:inline-block;margin-top:38px;border-radius:18px;box-shadow:inset 0 0 0 3px rgba(247,241,229,.7);padding:22px 30px;font:600 30px/1.35 Montserrat;max-width:880px">{d["sub"]}</div>
    </div>{foot()}''')

def slogan(d):
    """Seri: Slogan — ortalanmış dev iki parçalı ifade (soru + cevap), dar başlık fontu, alt alta iki buton.
    d: tag, l1, l2, l3, l4, sub, cta"""
    return post(f'''{glow(240,240,620,"#F95B1C")}{glow(-200,980,520,"#0B2345")}{arcs(-160,-160)}{arcs(720,900)}{tile()}
    <div style="position:absolute;left:64px;right:64px;top:150px;text-align:center"><span class="tag">{d["tag"]}</span></div>
    <div style="position:absolute;left:40px;right:40px;top:260px;text-align:center">
      <div class="osw" style="font-size:132px;line-height:.95">{d["l1"]}<br><span style="color:var(--o)">{d["l2"]}</span></div>
      <div style="width:160px;height:6px;background:var(--o);margin:40px auto"></div>
      <div class="osw" style="font-size:112px;line-height:.95">{d["l3"]}<br><span style="color:var(--o)">{d["l4"]}</span></div>
      <div style="font:800 30px/1.3 Montserrat;margin:38px auto 40px;text-transform:uppercase;letter-spacing:.04em;max-width:820px">{d["sub"]}</div>
      <div style="display:grid;gap:16px;justify-items:center"><span class="cta ol">Sınırlı kontenjan</span><span class="cta">{d["cta"]}</span></div>
    </div>{foot()}''')


# ---------- Kütüphane: yeni kompozisyon aileleri ve Story ----------
_LIB0 = library
def library():
    return _LIB0() + [
      ("07-slogan", slogan(dict(tag="2026–2027 hazırlık", l1="Hedefin", l2="büyük mü?", l3="Planın da", l4="büyük olsun.",
        sub="Sınav hazırlığı · yurt dışı eğitim planı", cta="Planını bizle oluştur"))),
      ("08-fotografli-duyuru", foto_duyuru(dict(kicker="Başvuru dönemi", h1="Başvurular", h2="başladı.", h3="Kaçırma!",
        sub="Okuluna ve programına göre son tarihini birlikte kontrol edelim."))),
      ("09-story", story(dict(tag="IELTS hazırlık", title=["Hedef bant", "için plan", "şimdi başlar."],
        body="Dört bölüm, tek takvim. Hedef okulunun istediği puandan geriye doğru çalış.", cta="DM 'IELTS' yaz"))),
    ]

META["intro"] = ("Sekiz Feed serisi ve bir Story düzeni. Seriler farklı kompozisyon ailelerinden oluşur: dev sayı, takvim, dev sınav adı, "
                 "numaralı carousel, istatistik kartları, uzman notu, ortalanmış slogan ve tam sayfa fotoğraflı duyuru. "
                 "Lacivert ikonlu iletişim bandı ve turuncu logo karosu her postta sabittir.")
META["series"] += [
  dict(id="07", name="Slogan", img=["07-slogan"], when="Bir dönemin ya da kampanyanın ana fikrini tek vurucu soru-cevapla söylemek.",
       freq="Dönem başlarında", fmt="Tek post · ortalanmış tipografi",
       slots=["Ortalanmış etiket", "Dar başlık fontu: soru (beyaz + turuncu)", "Turuncu ayırıcı, cevap (beyaz + turuncu)", "Alt alta iki buton: Sınırlı kontenjan + CTA"],
       caption="Hedefin büyük mü? Planın da büyük olsun. 🎯\n\nSınav hazırlığından başvuru dosyasına kadar her adımı hedef okuluna göre planlıyoruz.\n\nPlanını bizle oluştur.\n#ABAEğitim #YurtDışıEğitim #SınavHazırlık #Hedef2027"),
  dict(id="08", name="Fotoğraflı Duyuru", img=["08-fotografli-duyuru"], when="Başvuru dönemi, program açılışı gibi duyuruları güçlü bir kampüs görseliyle vermek.",
       freq="Dönem açılışlarında", fmt="Tek post · tam sayfa görsel",
       slots=["Tam sayfa fotoğraf (yüklenirse) ya da çizgisel kampüs silüeti", "Alttan lacivert geçiş", "Dev üç satır: beyaz / turuncu / beyaz", "Konturlu bilgi kutusu"],
       caption="Başvurular başladı. Kaçırma! 📌\n\nSon tarihler okula ve programa göre değişir. Hedef okulunun takvimini birlikte kontrol edelim.\n#ABAEğitim #ÜniversiteBaşvurusu #YurtDışıEğitim"),
  dict(id="09", name="Instagram Story", img=["09-story"], when="Feed postunu destekleyen tek ekranlık hatırlatma; 1080×1920.",
       freq="Feed postlarıyla birlikte", fmt="Story · 9:16",
       slots=["Üst ve alt güvenli alan boş", "Blok başlık, son satır turuncu", "Kısa açıklama + turuncu CTA", "Lacivert iletişim bandı"],
       caption="Story'de caption görünmez; öne çıkanlar notu: “IELTS hazırlık planı.” #ABAEğitim"),
]
