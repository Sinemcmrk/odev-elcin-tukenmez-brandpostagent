"""Seri tanımları: her seri bir ya da daha fazla şablon sayfasına dönüşür.

LLM yalnızca seri düzeyindeki alanları doldurur (başlık, metin, CTA...).
Sayfa sayısı, sayfa sırası, sabit etiketler gibi teknik değerleri kod hesaplar.
"""

class S:
    """Metin alanı. max: görünen karakter sınırı (HTML etiketleri hariç)."""
    def __init__(self, max, desc, req=True, html=False):
        self.max, self.desc, self.req, self.html = max, desc, req, html
    def doc(self):
        h = " HTML: yalnızca <b>, <br>" if self.html else ""
        return f"metin, en fazla {self.max} karakter. {self.desc}{h}{'' if self.req else ' (isteğe bağlı)'}"

class L:
    """Liste alanı."""
    def __init__(self, item, min, max, desc):
        self.item, self.min, self.max, self.desc = item, min, max, desc
    def doc(self):
        return f"liste ({self.min}–{self.max} öğe). {self.desc}. Her öğe: " + (self.item.doc() if not isinstance(self.item, O) else "nesne " + self.item.doc())

class O:
    """Nesne alanı."""
    def __init__(self, fields):
        self.fields = fields
    def doc(self):
        return "{" + "; ".join(f"{k}: {v.doc()}" for k, v in self.fields.items()) + "}"

def schema_doc(schema):
    return "\n".join(f"- {k}: {v.doc()}" for k, v in schema.items())


class Series:
    def __init__(self, brand, id, name, schema, build, example, kind="single", needs_facts=None, fixed_labels=(), fact_lists=()):
        self.brand, self.id, self.name, self.schema = brand, id, name, schema
        self.build, self.example, self.kind, self.needs_facts = build, example, kind, needs_facts
        self.fixed_labels = list(fixed_labels)   # şablonda sabit yazan etiketler (tekrar denetimi için)
        self.fact_lists = list(fact_lists)       # her öğesi kullanıcının bilgisinde geçmesi gereken liste alanları (ör. okullar)

# ------------------------------------------------------------------ ABA PSİKOLOJİ
def _ps_mit(f):
    n = 2 + len(f["myths"]); pages = [("mit_kapak", dict(n=n, tag=f["tag"], l1=f["l1"], l2=f["l2"], l3=f["l3"], body=f["body"], cta=f["cta"] + " →"))]
    for k, m in enumerate(f["myths"]):
        pages.append(("mit_sayfa", dict(n=n, i=k + 1, myth=m["myth"], fact=m["fact"], note=m["note"],
                                        swipe="ÖZET İÇİN KAYDIR →" if k == len(f["myths"]) - 1 else "BİR SONRAKİ MİT İÇİN KAYDIR →")))
    pages.append(("kapanis", dict(n=n, tag=f["close_tag"], body=f["close_body"], list=f["close_list"], box=f["close_box"], cta=f["close_cta"] + " →")))
    return pages

PSIKOLOJI = [
  Series("aba_psikoloji", "ic_ses", "İç Ses", {
      "tag": S(22, "duygu adı, ör. 'İç ses', 'Kararsızlık'"),
      "quote": L(S(16, "satır"), 2, 3, "öğrencinin birinci tekil iç sesi, satırlara bölünmüş"),
      "label": S(22, "kart etiketi, ör. 'Karşılaştırma'"),
      "body": S(110, "“X değil, Y” yeniden çerçeveleme cümlesi; vurgu <b> içinde", html=True),
      "cta": S(34, "fiil + 'birlikte', ok işareti koyma")},
    lambda f: [("ic_ses", dict(f))],
    dict(tag="İç ses", quote=["Herkes benden", "daha hızlı", "ilerliyor."], label="Karşılaştırma",
         body="Bu düşünce yetersizlik değil; <b>kendi ritmini kaybettiğinin</b> işareti olabilir.", cta="Kendi ritmini birlikte bulalım")),
  Series("aba_psikoloji", "ebeveyn", "Ebeveyn Rehberi", {
      "headline": L(S(20, "satır"), 2, 3, "'Çocuğunuz … ise' durumu, satırlara bölünmüş, son satır '...' ile bitebilir"),
      "q": S(34, "turuncu kutudaki asıl soru; iki kısa satır için <br>", html=True),
      "body": S(130, "veliye 'siz' diye hitap; “X değil, Y” + ilk cümle önerisi", html=True),
      "cta": S(26, "ör. 'Birlikte konuşalım'")},
    lambda f: [("ebeveyn", dict(f))],
    dict(headline=["Çocuğunuz sınav", "sonucunu sizden", "saklıyorsa..."], q="Notu mu, yoksa<br>tepkinizi mi?",
         body="Sakladığı şey not değil, <b>sizin tepkinize dair korkusu</b> olabilir. İlk cümleniz “Nasıl hissediyorsun?” olsun.", cta="Birlikte konuşalım")),
  Series("aba_psikoloji", "mit", "Mit vs Gerçek", {
      "tag": S(30, "kapak etiketi, ör. 'Doğru bildiğimiz yanlışlar'"),
      "l1": S(10, "kapak başlığı 1. satır (mürekkep)"), "l2": S(10, "2. satır (bordo)"), "l3": S(12, "3. satır (turuncu)"),
      "body": S(70, "kapak açıklaması"), "cta": S(24, "ör. 'Birlikte ayıralım'"),
      "myths": L(O({"myth": S(80, "yaygın yanlış inanış, birinci tekil"), "fact": S(70, "doğru bilgi"), "note": S(60, "kısa açıklama")}), 2, 3, "mit/gerçek çiftleri"),
      "close_tag": S(20, "kapanış etiketi"), "close_body": S(70, "kapanış cümlesi"),
      "close_list": L(S(18, "tek fiil ya da kısa emir"), 3, 4, "özet nokta listesi"),
      "close_box": S(40, "koyu kutu metni, iki satır için <br>", html=True), "close_cta": S(12, "ör. 'Bize yaz'")},
    _ps_mit,
    dict(tag="Doğru bildiğimiz yanlışlar", l1="Sınav", l2="gecesi", l3="mitleri", body="Sınav haftasında en sık duyduğumuz iki cümleyi ayırıyoruz.", cta="Birlikte ayıralım",
         myths=[dict(myth="Sınavdan önceki gece sabahlarsam daha çok konu yetiştiririm.", fact="Uyku, gün içinde öğrendiklerini hafızaya yerleştirir.", note="Son gece yeni konu değil, dinlenmiş bir zihin kazandırır."),
                dict(myth="Kaygı hissediyorsam yeterince hazır değilimdir.", fact="Orta düzeyde kaygı, dikkati toplamaya yardım eder.", note="Hedef kaygıyı yok etmek değil, yönetmek.")],
         close_tag="Sınav haftası", close_body="Son gece için dört küçük karar, büyük bir fark yaratır.", close_list=["Uyu", "Tekrar et, yükleme", "Nefes al", "Kendine güven"],
         close_box="Sınav dönemini<br>birlikte planlayalım", close_cta="Bize yaz"),
    kind="carousel"),
  Series("aba_psikoloji", "rutin", "Haftanın Rutini", {
      "tag": S(24, "gün/mevsim girişi, ör. 'Pazartesi enerjisi'"),
      "l1": S(12, "başlık 1. satır"), "l2": S(12, "2. satır (bordo)"), "l3": S(12, "3. satır (turuncu)"),
      "voice": S(50, "bordo kutudaki iç ses cümlesi, tırnaksız"),
      "steps": L(S(48, "uygulanabilir adım"), 3, 3, "üç küçük adım"),
      "line": S(45, "adaçayı renkli özet satırı"), "cta": S(32, "fiil + 'birlikte'")},
    lambda f: [("rutin", dict(f))],
    dict(tag="Pazartesi enerjisi", l1="Yeni hafta", l2="yeni bir", l3="plan", voice="Bu hafta her şeye yetişmem lazım.",
         steps=["Haftanın tek önceliğini seç.", "Her güne kısa bir çalışma bloğu koy.", "Cuma akşamı neyin işe yaradığını yaz."], line="Plan küçüldükçe kaygı da küçülür.", cta="Haftanı birlikte planlayalım")),
  Series("aba_psikoloji", "uzman", "Uzman Notu (blog duyurusu)", {
      "title": S(22, "serif başlık 1. satır"), "title2": S(40, "2. satır, alev turuncu"),
      "summary": S(80, "'Bu yazıda' özeti, tek cümle")},
    lambda f: [("uzman", dict(byline="UZMAN NOTU · ABA PSİKOLOJİ", **f))],
    dict(title="Tercih Döneminde", title2="Kim Konuşuyor, Kim Dinliyor?", summary="Tercih konuşmalarında gencin sesine alan açmanın üç yolu.")),
]

# ------------------------------------------------------------------ ABA EĞİTİM
def _eg_keske(f):
    r = f["rules"]; n = 4
    return [("keske_kapak", dict(n=n, tag=f["tag"], h=f["h"], body=f["body"], cta="Kaydet • sonra dön")),
            ("keske_sayfa", dict(n=n, i=1, tag="İlk 2 kural", h=f["page1_title"], sum=f["page1_sum"], rows=[("01", r[0]["h"], r[0]["p"]), ("02", r[1]["h"], r[1]["p"])])),
            ("keske_sayfa", dict(n=n, i=2, tag="Son 2 detay", h=f["page2_title"], sum=f["page2_sum"], rows=[("03", r[2]["h"], r[2]["p"]), ("04", r[3]["h"], r[3]["p"])])),
            ("keske_son", dict(n=n, body=f["close_body"]))]

EGITIM = [
  Series("aba_egitim", "keske", "“Keşke” Listesi", {
      "tag": S(22, "kapak etiketi"), "h": S(60, "kapak başlığı; 3–4 satır için <br>, vurgu <em>", html=True),
      "body": S(90, "kapak açıklaması"),
      "rules": L(O({"h": S(40, "kural başlığı"), "p": S(90, "kısa açıklama, öğrenciye 'sen'")}), 4, 4, "tam 4 kural"),
      "page1_title": S(30, "2. sayfa başlığı, ör. 'İlk 2<br><em>şaşırtan kural</em>'", html=True), "page1_sum": S(30, "2. sayfa özet hapı"),
      "page2_title": S(30, "3. sayfa başlığı", html=True), "page2_sum": S(30, "3. sayfa özet hapı"),
      "close_body": S(90, "kapanış cümlesi")},
    _eg_keske,
    dict(tag="ABD başvurusu", h="ABD başvurusunda<br><em>“keşke”</em> dedirten<br>4 şey", body="Başvuru sezonu başladı. Bu dört detayı şimdiden bil.",
         rules=[dict(h="Ana essay'in bir kelime sınırı var", p="Her cümle bir karar. Hikâyeni tek bir ana fikre indir."),
                dict(h="Tavsiye mektubu erken istenir", p="Öğretmenine haftalar önceden haber ver."),
                dict(h="Aktivite listesi sınırlı", p="Sayı değil derinlik: en güçlü aktivitelerini öne al."),
                dict(h="“Test-optional” sınavsız demek değil", p="Okul politikasını tek tek kontrol et.")],
         page1_title="İlk 2<br><em>şaşırtan kural</em>", page1_sum="Ana fikir = essay'in omurgası", page2_title="Son 2<br><em>kritik detay</em>", page2_sum="Derinlik > sayı",
         close_body="Hedefin büyük mü? Planın da büyük olsun. Başvuru takvimini birlikte kuralım."),
    kind="carousel"),
  Series("aba_egitim", "sinav", "Sınav Programı", {
      "exam1": S(10, "sınav adı 1. satır (dar, BÜYÜK)"), "exam2": S(8, "2. satır (turuncu)"),
      "sub": S(34, "alt başlık, ör. 'Doğru stratejiyle hazırlan.'"),
      "pill": S(28, "sınav biçimi; YALNIZCA doğrulanmış bilgi verilmişse, yoksa boş bırak", req=False),
      "feat": L(S(34, "programın bir adımı"), 4, 4, "dört madde"), "cta": S(26, "ör. 'Planını bizle oluştur'")},
    lambda f: [("sinav", dict(f))],
    dict(exam1="Digital", exam2="SAT", sub="Doğru stratejiyle hazırlan.", pill="", feat=["Diagnostik deneme ile başlangıç", "Kişisel çalışma planı", "Modül bazlı ders ve tekrar", "Düzenli deneme ve analiz"], cta="Planını bizle oluştur")),
  Series("aba_egitim", "uzman", "Uzman Serisi (blog duyurusu)", {
      "h1": S(14, "başlık 1. satır (dar, BÜYÜK)"), "h2": S(14, "2. satır (turuncu)"), "body": S(110, "tek paragraf özet")},
    lambda f: [("uzman", dict(tag="Uzman serisi", meta="BLOG", **f))],
    dict(h1="Yüksek puan", h2="yetmez.", body="Başvuru dosyası bir hikâye anlatır. Puan kapıyı aralar; seni içeri alan, o hikâyedir.")),
  Series("aba_egitim", "son_tarih", "Son Tarih", {
      "day": S(10, "gün ve ay, ör. '1 KASIM' — yalnızca doğrulanmış bilgiden"), "year": S(4, "yıl"),
      "what": S(70, "neyin son tarihi; iki satır için <br>", html=True),
      "checks": L(S(40, "kontrol sorusu"), 3, 3, "kontrol listesi"), "cta": S(40, "DM anahtar kelimesi ile, ör. 'DM “TAKVİM” yaz • yol haritanı al'")},
    lambda f: [("son_tarih", dict(f, note="Tarihler okula göre değişebilir; hedef okulunun sitesinden doğrula."))],
    dict(day="1 KASIM", year="2026", what="ABD erken başvuru<br>Early Decision · Early Action", checks=["Common App hesabın hazır mı?", "Ana essay son okumada mı?", "Tavsiye mektupları istendi mi?"], cta="DM “TAKVİM” yaz • yol haritanı al"),
    needs_facts="tarih (gün, ay, yıl ve neyin son tarihi olduğu)"),
  Series("aba_egitim", "kabul", "Kabul Duyurusu", {
      "tag": S(22, "etiket"), "num": S(5, "kabul sayısı — YALNIZCA kullanıcının verdiği sayı; marka bilgilerindeki geçmiş sayıları kullanma"),
      "line1": S(14, "sayıdan sonraki kelime"), "italic": S(18, "light italik vurgu"), "line2": S(12, "cümle sonu"),
      "schools": L(S(12, "okul kısa adı"), 0, 5, "okullar — YALNIZCA kullanıcının doğrulanmış bilgisinde geçen okullar; bilgi yoksa boş liste []"),
      "body": S(90, "yöntem cümlesi"), "cta": S(30, "yorum çağrısı")},
    lambda f: [("kabul", dict(f))],
    dict(tag="Kabul sonuçları", num="221", line1="öğrencimiz", italic="o e-postayı", line2="aldı.", schools=["OXFORD", "CAMBRIDGE", "IMPERIAL", "LSE", "UCL"], body="Tesadüf değil, plan. Üç yıllık bir yöntem, tek bir danışmanlık odası.", cta="Yoruma hedef okulunu yaz"),
    needs_facts="kabul sayısı ve okul adları", fact_lists=["schools"]),
]

# ------------------------------------------------------------------ E4I
def _e4i_play(f):
    n = 4; s = f["steps"]
    pages = [("play_cover", dict(n=n, tag=f["tag"], h=f["h"], steps=[x["step"] for x in s]))]
    for k, x in enumerate(s):
        d = dict(n=n, i=k + 1, step=x["step"], h1=x["h1"], h2=x["h2"], rows=x["rows"], end=x["end"])
        if k == 2: d.update(btn=True, end="Save this playbook.")
        pages.append(("play_step", d))
    return pages

E4I = [
  Series("e4i", "playbook", "Playbook (3 steps)", {
      "tag": S(24, "cover tag, e.g. 'A 3-step playbook'"),
      "h": S(50, "cover headline; 3 lines with <br>; last line wrapped in <span class='o'>…</span>", html=True),
      "steps": L(O({"step": S(8, "one-word step name"), "h1": S(12, "headline line 1"), "h2": S(14, "headline line 2 (orange)"),
                     "rows": L(S(32, "short imperative"), 3, 3, "three rows"), "end": S(32, "lime lesson line, e.g. 'Proof beats promises.'")}), 3, 3, "exactly 3 steps")},
    _e4i_play,
    dict(tag="A 3-step playbook", h="How to land<br>your first<br><span class='o'>internship.</span>",
         steps=[dict(step="Map", h1="Before", h2="you apply.", rows=["List 10 teams you admire.", "Find one problem they have.", "Write it in one line."], end="Curiosity beats credentials."),
                dict(step="Prove", h1="Prove it", h2="small.", rows=["Build one tiny project.", "Share it in public.", "Ask for one piece of feedback."], end="Proof beats promises."),
                dict(step="Ask", h1="Send", h2="the email.", rows=["Five sentences. No more.", "Link the project.", "End with one clear ask."], end="Save this playbook.")]),
    kind="carousel"),
  Series("e4i", "field", "Future Careers", {
      "f1": S(12, "career FIELD / discipline name, line 1. Must be a real field of study or work (e.g. 'Urban air', 'Synthetic'), "
                  "never a single product or gadget: if the topic is a product (e.g. flying cars), name the field behind it (e.g. 'Urban air' / 'mobility')"),
      "f2": S(12, "field name line 2 (lime)"), "line": S(70, "one-line definition of what people in this field do"),
      "bars": L(L(S(28, "text"), 2, 2, "[key, value]"), 3, 3,
                "three bars: [Skills, school subjects/skills], [Where, sectors], [Start, a concrete first step a high-school student can take alone, "
                "e.g. 'A free online course' or 'Build a small model'; do not invent E4I programs, dates or prizes]"),
      "end": S(40, "lime closing line, e.g. \"Today's field: tomorrow's career.\" Must NOT repeat the fixed top tag "
                   "\"Future careers: fields you haven't met yet\" or any other text on the post")},
    lambda f: [("field", dict(f, bars=[(c, b[0], b[1]) for c, b in zip("gpo", f["bars"])]))],
    dict(f1="Synthetic", f2="biology", line="Designing living systems the way engineers design machines.", bars=[["Skills", "Biology + code + design"], ["Where", "Health · Climate · Food"], ["Start", "A summer lab project"]], end="Today's field: tomorrow's career."),
    fixed_labels=["Future careers: fields you haven't met yet", "Today's field"]),
  Series("e4i", "study", "Study Smarter", {
      "tag": S(16, "tag, e.g. 'Study tip'"), "h1": S(16, "headline line 1"), "h2": S(14, "line 2 (orange)"),
      "rows": L(S(34, "short tip"), 3, 3, "three tips"), "end": S(36, "lime rule line")},
    lambda f: [("study", dict(f))],
    dict(tag="Study tip", h1="Study smarter,", h2="not longer.", rows=["Review after 1, 3 and 7 days.", "Test yourself before you reread.", "Sleep on it."], end="Spaced repetition beats cramming.")),
  Series("e4i", "manifesto", "Manifesto", {
      "l1": S(14, "statement line 1"), "l2": S(16, "line 2"), "l3": S(16, "line 3 (orange)"),
      "tr": S(90, "Turkish translation of the statement"), "cta": S(36, "outline CTA")},
    lambda f: [("manifesto", dict(f))],
    dict(l1="Innovation", l2="isn't a talent.", l3="It's a mindset.", tr="İnovasyon bir yetenek değil, geliştirilebilen bir zihniyettir.", cta="Follow for global opportunities.")),
  Series("e4i", "program", "Program Spotlight", {
      "tag": S(22, "tag"), "h": S(50, "headline; 3 lines with <br>; last line in <span class='o'>…</span>", html=True),
      "bars": L(L(S(30, "text"), 2, 2, "[key, value]"), 3, 3, "three bars: format, who, focus"), "cta": S(30, "e.g. 'Apply via link in bio'")},
    lambda f: [("program", dict(f, bars=[(c, b[0], b[1]) for c, b in zip("gpo", f["bars"])]))],
    dict(tag="Program spotlight", h="48 hours.<br>From idea<br><span class='o'>to prototype.</span>", bars=[["Format", "Team hackathon"], ["Who", "High school & university"], ["Focus", "AI · Life sciences · Startups"]], cta="Apply via link in bio"),
    needs_facts="program details (format, who, dates) unless it is one of E4I's verified programs"),
]

# ------------------------------------------------------------------ DESIGN HOUSE
def _dh_dest(f):
    n = 1 + len(f["cities"])
    pages = [("dest_cover", dict(n=n, bg="<br>".join(c["city"].upper() for c in f["cities"]), h=f["h"], sub=f["sub"]))]
    for k, c in enumerate(f["cities"]):
        d = dict(n=n, i=k + 1, city=c["city"], where=c["city"], schools=c["schools"], line=c["line"], bgsize=200 if len(c["city"]) > 7 else 250)
        if k == len(f["cities"]) - 1: d["end"] = f["end"]
        pages.append(("dest_city", d))
    return pages

DESIGN = [
  Series("design_house", "lesson", "Portfolio Lesson", {
      "lab": S(26, "DM Mono label, e.g. '( Portfolio lesson )'"), "h1": S(18, "condensed headline line 1"), "h2": S(22, "gold line 2"),
      "body": S(90, "why reviewers care"), "rule": S(60, "one concrete rule (gold)"), "cta": S(34, "gold CTA")},
    lambda f: [("lesson", dict(f))],
    dict(lab="( Portfolio lesson )", h1="Show the turn.", h2="Not just the end.", body="Reviewers want to see where your idea changed direction, and why.", rule="2–3 pages that show a pivot, labeled by date.", cta="Explore your creative direction.")),
  Series("design_house", "statement", "Studio Notes (X — Y.)", {
      "lab": S(20, "label, e.g. '( Studio notes )'"), "l1": S(18, "statement part 1 (before the dash)"), "l2": S(28, "part 2 (gold)"), "sub": S(100, "one-sentence follow-up")},
    lambda f: [("statement", dict(f))],
    dict(lab="( Studio notes )", l1="Your first idea", l2="is rarely your best one.", sub="Keep it. Then make three more. The fourth one usually knows what it wants to be.")),
  Series("design_house", "future", "Build Your Future (CTA)", {
      "body": S(110, "one-line offer"), "cta": S(44, "mono DM call to action, e.g. 'DM “REVIEW” to book a portfolio review'")},
    lambda f: [("future", dict(f))],
    dict(body="Portfolio prep, mentorship and admissions strategy for the world's best art & design schools.", cta="DM “REVIEW” to book a portfolio review")),
  Series("design_house", "destinations", "Destinations", {
      "h": S(30, "cover headline, 3 lines with <br>", html=True), "sub": S(44, "cover subline"),
      "cities": L(O({"city": S(9, "city name"), "schools": S(30, "schools from verified list, 2 lines with <br>", html=True), "line": S(60, "one original line about the city")}), 2, 3, "cities"),
      "end": S(44, "gold closing CTA on last slide")},
    _dh_dest,
    dict(h="Where our<br>students<br>get in.", sub="Three cities. Six schools. One studio.",
         cities=[dict(city="London", schools="Central Saint<br>Martins + RCA.", line="Where a portfolio is read like a point of view."),
                 dict(city="New York", schools="Parsons<br>+ Pratt.", line="Two schools where making is a way of thinking."),
                 dict(city="Milan", schools="Politecnico<br>+ NABA.", line="Design culture with a technical spine.")],
         end="Build your application with Design House."),
    kind="carousel"),
]


# ------------------------------------------------------------------ KÜTÜPHANEDEKİ DİĞER SERİLER + YENİ KOMPOZİSYON AİLELERİ
def _ps_pasaport(f):
    return [("pasaport_kapak", dict(code=f["code"], full=f["full"], desc=f["desc"], pill=f["pill"])),
            ("pasaport_ic", dict(code=f["code"], boxes=[(b["h"], b["p"]) for b in f["boxes"]])),
            ("pasaport_son", dict(q=f["q"], chips=f["chips"]))]

PSIKOLOJI += [
  Series("aba_psikoloji", "pasaport", "Sınav Pasaportu", {
      "code": S(6, "sınavın kısa adı, ör. IELTS"), "full": S(52, "açılımı, iki satır için <br>", html=True),
      "desc": S(90, "sınavı tek cümlede tanıt"), "pill": S(24, "bölüm/puan bilgisi — YALNIZCA kullanıcının bilgisinden"),
      "boxes": L(O({"h": S(18, "kutu başlığı"), "p": S(110, "kutu metni; üçüncü kutu psikolojik hazırlık önerisi")}), 3, 3, "Kimler için? / Ne ölçer? / Hazırlık vizesi"),
      "q": S(64, "kapanış sorusu, satırlar için <br>", html=True), "chips": L(S(12, "seçenek"), 4, 4, "yorum seçenekleri (ör. bölüm adları)")},
    _ps_pasaport,
    dict(code="IELTS", full="International English<br>Language Testing System", desc="Yurt dışında eğitim için en yaygın İngilizce yeterlik sınavlarından biri.",
         pill="4 BÖLÜM • 0–9 BANT", boxes=[dict(h="Kimler için?", p="Birleşik Krallık, Avustralya, Kanada ve daha birçok ülkede okumak isteyen öğrenciler."),
         dict(h="Ne ölçer?", p="Dinleme, okuma, yazma ve konuşma. Her bölüm ayrı bir bant puanı alır."),
         dict(h="Hazırlık vizesi", p="Konuşma bölümündeki kaygı çok yaygındır. Günde 5 dakika sesli pratik, bu kaygıyı küçültür.")],
         q="Senin IELTS<br>hazırlığında<br>en zor bölüm hangisi?", chips=["Listening", "Reading", "Writing", "Speaking"]),
    kind="carousel", needs_facts="sınavın resmi bilgileri (bölüm sayısı, puan aralığı)"),
  Series("aba_psikoloji", "soru_bant", "Soru Bandı", {
      "tag": S(26, "konu etiketi"), "q": L(S(20, "satır"), 2, 3, "turuncu banttaki büyük soru, satırlara bölünmüş"),
      "sub": S(80, "koyu banttaki kısa cevap ipucu"), "cta": S(14, "ör. 'Kaydır', 'Bize yaz'")},
    lambda f: [("soru_bant", dict(f))],
    dict(tag="Okulun ilk haftaları", q=["Dikkati mi dağınık,", "yöntemi mi yanlış?"], sub="Odaklanamamak çoğu zaman irade değil, yöntem meselesidir.", cta="Kaydır")),
  Series("aba_psikoloji", "alinti", "Alıntı Kartı", {
      "q1": S(48, "normalleştiren cümlenin ilk yarısı (mürekkep)"), "q2": S(60, "ikinci yarısı (bordo vurgu)"),
      "line": S(70, "kısa nefes / öneri cümlesi")},
    lambda f: [("alinti", dict(f))],
    dict(q1="Kaygı, yolun kapandığını değil;", q2="bu yolun senin için önemli olduğunu söyler.", line="Nefes al ve yalnızca bir sonraki adımına dön.")),
]

EGITIM += [
  Series("aba_egitim", "veri", "Sayılarla", {
      "tag": S(20, "etiket"), "title": S(16, "program/sınav adı"), "sub": S(30, "light italik alt başlık"),
      "stats": L(O({"a": S(5, "sayı — YALNIZCA kullanıcının bilgisinden"), "b": S(34, "sayının açıklaması")}), 3, 3, "üç sayı kartı"),
      "body": S(110, "planlama cümlesi"), "cta": S(32, "DM anahtar kelime CTA'sı"), "src": S(40, "Kaynak: …")},
    lambda f: [("veri", dict(f, stats=[(x["a"], x["b"]) for x in f["stats"]]))],
    dict(tag="Sayılarla", title="IB Diploma", sub="üç sayıda bir program", stats=[dict(a="45", b="en yüksek toplam puan"), dict(a="24", b="diploma için en düşük puan"), dict(a="3", b="çekirdek: TOK · EE · CAS")],
         body="Hedef okulunun istediği puanı bil; planını o sayıdan geriye doğru kur.", cta="DM “IB” yaz · ücretsiz rehberlik", src="Kaynak: ibo.org"),
    needs_facts="sayılar ve kaynağı"),
  Series("aba_egitim", "slogan", "Slogan", {
      "tag": S(22, "etiket"), "l1": S(12, "soru 1. satır (beyaz)"), "l2": S(12, "soru 2. satır (turuncu)"),
      "l3": S(12, "cevap 1. satır (beyaz)"), "l4": S(14, "cevap 2. satır (turuncu)"), "sub": S(48, "küçük büyük-harf alt satır"), "cta": S(26, "turuncu buton")},
    lambda f: [("slogan", dict(f))],
    dict(tag="Yeni dönem hazırlık", l1="Hedefin", l2="büyük mü?", l3="Planın da", l4="büyük olsun.", sub="Sınav hazırlığı · yurt dışı eğitim planı", cta="Planını bizle oluştur")),
  Series("aba_egitim", "foto_duyuru", "Fotoğraflı Duyuru", {
      "kicker": S(20, "etiket"), "h1": S(11, "1. satır"), "h2": S(11, "2. satır (turuncu)"), "h3": S(11, "3. satır"),
      "sub": S(80, "konturlu kutudaki bilgi; tarih yalnızca kullanıcı verdiyse")},
    lambda f: [("foto_duyuru", dict(f))],
    dict(kicker="Başvuru dönemi", h1="Başvurular", h2="başladı.", h3="Kaçırma!", sub="Okuluna ve programına göre son tarihini birlikte kontrol edelim.")),
]

E4I += [
  Series("e4i", "cities", "Global Network", {
      "h1": S(14, "headline line 1"), "h2": S(18, "line 2 (orange)"), "end": S(30, "green bar summary")},
    lambda f: [("cities", dict(f, cities=["San Francisco", "Boston", "New York", "Toronto", "London", "Dublin", "Amsterdam", "Berlin", "Milan", "Geneva", "Dubai", "Istanbul"]))],
    dict(h1="Opportunities", h2="around the world.", end="12 cities. One network.")),
  Series("e4i", "process", "Process Infographic", {
      "kicker": S(30, "small spaced label"), "h1": S(16, "headline line 1"), "h2": S(18, "line 2 (lime), usually a question or key word"),
      "line": S(80, "one-line promise"), "steps": L(S(10, "one-word step label"), 4, 5, "steps of the process, in order")},
    lambda f: [("process", dict(f))],
    dict(kicker="EDUCATION FOR INNOVATION", h1="What is a", h2="hackathon?", line="From a real problem to a working prototype, in five moves.", steps=["Problem", "People", "Plan", "Prototype", "Pitch"])),
  Series("e4i", "spotlight", "Innovation Spotlight", {
      "tag": S(24, "purple tag"), "h1": S(16, "headline line 1"), "h2": S(18, "line 2 (orange)"),
      "sub": S(80, "what it is, in one sentence; no invented company news, numbers or dates"), "chips": L(S(22, "chip"), 2, 2, "[field, first step]")},
    lambda f: [("spotlight", dict(f))],
    dict(tag="Innovation spotlight", h1="Robots that", h2="learn by watching.", sub="Imitation learning lets machines copy a task from a few human demonstrations.", chips=["AI + robotics", "Try: a simulation lab"])),
]

DESIGN += [
  Series("design_house", "paths", "Six Paths", {
      "h": S(30, "headline, two lines with <br>", html=True), "cta": S(26, "mono arrow link")},
    lambda f: [("paths", dict(f, paths=[("Spatial<br>design", "Architecture", "#A9D6E5"), ("Visual<br>comms", "Graphic & type", "#EC6242"), ("Fine<br>arts", "Studio practice", "#F0E2A6"),
                                         ("Indus-<br>trial", "Product & object", "#D8F24A"), ("Fashion", "Concept & textile", "#C9C2F0"), ("Photo<br>&amp; film", "Storytelling", "#A9D6E5")]))],
    dict(h="Six creative<br>paths.", cta="Find your path -&gt;")),
  Series("design_house", "numbers", "By the Numbers", {
      "end": S(34, "closing line"), "it": S(24, "witty italic coral ending")},
    lambda f: [("numbers", dict(f, rows=[("12+", "Years"), ("900+", "Students"), ("40+", "Schools"), ("96%", "Accepted")]))],
    dict(end="Twelve years of portfolios,", it="zero boring ones.")),
  Series("design_house", "service", "Service Block", {
      "idx": S(2, "two-digit index 01–06"), "lab": S(24, "( label ) in DM Mono"), "title": S(28, "Archivo headline, two lines with <br>", html=True),
      "body": S(120, "what the service does"), "cta": S(28, "mono arrow link")},
    lambda f: [("service", dict(f))],
    dict(idx="01", lab="( What we do ) 01", title="Portfolio<br>direction.", body="We help you find the thread that connects your projects, then edit until every page earns its place.", cta="Book a portfolio review")),
  Series("design_house", "badge", "Badge Lesson", {
      "kicker": S(60, "gold mono kicker"), "h1": S(14, "headline line 1"), "h2": S(14, "line 2"), "h3": S(16, "line 3 (gold)"),
      "rule": S(26, "the rule on the badge, 2–3 short lines with <br>; no invented numbers", html=True), "body": S(90, "one-sentence explanation")},
    lambda f: [("badge", dict(f))],
    dict(kicker="Nobody asks what software you used for the cover.", h1="Open with", h2="a decision,", h3="not decoration.", rule="One idea.<br>One cover.",
         body="The first page tells the reviewer how you think. Make it a choice, not a collage.")),
]

# Kompozisyon aileleri: Agent 1'in aday seçimi, alternatif önerisi ve çeşitlilik kontrolü bu bilgiyi kullanır.
# layout: yerleşim tipi (çeşitlilik ölçüsü) · use: hangi içerik türünde · photo: fotoğraf kullanımı
FAMILY = {
  "ic_ses": ("kart", "Koyu iç ses kartı: tırnaklı birinci tekil cümle + yeniden çerçeveleyen cam kart", "öğrencinin duygusu, kaygı, kıyaslama", "yok"),
  "ebeveyn": ("soru-kutusu", "Veli sorusu: büyük durum cümlesi + turuncu soru kutusu + beyaz açıklama kartı", "veli iletişimi, aile", "yok"),
  "mit": ("carousel-karşılaştırma", "Mit vs Gerçek carousel'i: kapak + mit/gerçek kartları + kapanış listesi", "yanlış bilinenler, karşılaştırma", "yok"),
  "pasaport": ("carousel-illüstrasyon", "Sınav Pasaportu: pasaport illüstrasyonlu kapak + numaralı kutular + seçenek çipleri", "bir sınavı tanıtma (resmi bilgi gerekir)", "yok"),
  "rutin": ("adım-listesi", "Haftalık rutin: üç renkli başlık + iç ses kutusu + numaralı 3 adım", "motivasyon, plan, rutin", "yok"),
  "uzman": ("bölünmüş-editoryal", "Uzman notu: beyaz üst + serif başlık, alev turuncu alt blok", "blog yazısı duyurusu", "yok"),
  "soru_bant": ("renk-bantları", "Soru bandı: üstte görsel alan, ortada turuncu soru bandı, altta koyu kaydırma bandı", "tek soru, merak, carousel kapağı dili", "isteğe bağlı"),
  "alinti": ("ortalanmış-alıntı", "Alıntı kartı: zemin üzerinde ortalanmış kart, büyük tırnak, iki renkli cümle", "sakinleştirici kısa mesaj, mindfulness", "isteğe bağlı"),
  "keske": ("carousel-numaralı", "“Keşke” listesi carousel'i: kapak + turuncu numara blokları + 3 butonlu kapanış", "başvuru ipuçları, hatalar", "yok"),
  "sinav": ("dev-başlık", "Sınav programı: dev dar sınav adı + madde listesi + iki buton", "sınav hazırlık programı duyurusu", "yok"),
  "uzman_e": ("illüstrasyon-editoryal", "Uzman serisi: bordo zemin, çizgisel bina, dar başlık", "blog yazısı duyurusu", "yok"),
  "son_tarih": ("takvim", "Son tarih: dev tarih + krem kontrol listesi", "başvuru takvimi (tarih gerekir)", "yok"),
  "kabul": ("dev-sayı", "Kabul duyurusu: dev turuncu sayı + okul bandı", "kabul sonuçları (doğrulanmış bilgi gerekir)", "yok"),
  "veri": ("istatistik-kartları", "Sayılarla: başlık + üç sayı kartı + kaynak", "program/sınav sayıları (doğrulanmış bilgi gerekir)", "yok"),
  "slogan": ("ortalanmış-tipografi", "Slogan: ortalanmış dev soru-cevap, alt alta iki buton", "kampanya ana fikri, motivasyon, danışmanlık", "yok"),
  "foto_duyuru": ("tam-sayfa-görsel", "Fotoğraflı duyuru: tam sayfa görsel, alttan geçiş, dev üç satır", "dönem açılışı, başvuru duyurusu", "isteğe bağlı"),
  "program": ("sanat-bandı-bilgi", "Program spotlight: halka bandı + başlık + üç renkli bilgi çubuğu", "E4I programı duyurusu (bilgi gerekir)", "yok"),
  "playbook": ("carousel-adım", "Playbook carousel'i: kapak + üç adım kartı", "beceri öğretme, rehber", "yok"),
  "field": ("alan-kartı", "Future Careers: dev alan adı + üç bilgi çubuğu", "yeni bir meslek alanı", "yok"),
  "cities": ("ızgara", "Global Network: başlık + 12 şehir ızgarası", "uluslararası ağ, fırsatlar", "yok"),
  "study": ("numaralı-ipucu", "Study Smarter: başlık + üç renkli numaralı satır", "çalışma ipucu", "yok"),
  "manifesto": ("manifesto-tipografi", "Manifesto: dev tırnak + üç satırlık ifade", "vizyon, değerler", "yok"),
  "process": ("ikonlu-infografik", "Süreç infografiği: başlık + ikonlu, bağlantılı 4–5 adım", "bir süreci/kavramı açıklama", "yok"),
  "spotlight": ("büyük-görsel", "Innovation spotlight: üstte büyük görsel alan, altta başlık ve çipler", "teknoloji, yenilik, fikir tanıtımı", "isteğe bağlı"),
  "lesson": ("pano-ders", "Portfolio lesson: iğnelenmiş sayfa çizimi + dar başlık + altın kural", "tek portfolyo kuralı", "yok"),
  "statement": ("ifade-tipografi", "Studio notes: iki parçalı “X — Y.” ifadesi", "kısa fikir, motivasyon", "yok"),
  "future": ("siyah-cta", "Build your future: dev Archivo başlık + DM CTA", "danışmanlık çağrısı", "yok"),
  "destinations": ("carousel-şehir", "Destinations carousel'i: konturlu şehir adları + okul çiftleri", "hedef okullar, şehirler", "yok"),
  "paths": ("pastel-ızgara", "Six paths: krem zemin, altı pastel disiplin kartı", "yaratıcı disiplinler, bölüm seçimi", "yok"),
  "numbers": ("sayı-bandı", "By the numbers: lavanta bant + dört büyük sayı (web sitesi verisi)", "kurum kanıtı, güven", "yok"),
  "service": ("bölünmüş-blok", "Service block: krem zemin, solda görsel panel, sağda mercan rakam + başlık", "bir hizmeti anlatma", "isteğe bağlı"),
  "badge": ("rozet", "Badge lesson: dev dar başlık + dönük altın rozet", "sayılı/somut portfolyo kuralı", "isteğe bağlı"),
  "story": ("story", "Instagram Story: dikey tek ekran, büyük başlık + kısa metin + CTA", "hızlı hatırlatma", "yok"),
}

def family(series):
    key = "uzman_e" if (series.id == "uzman" and series.brand == "aba_egitim") else series.id
    lay, desc, use, photo = FAMILY.get(key, ("diğer", series.name, "", "yok"))
    return {"layout": lay, "desc": desc, "use": use, "photo": photo}

ALL = {"aba_psikoloji": PSIKOLOJI, "aba_egitim": EGITIM, "e4i": E4I, "design_house": DESIGN}

# ------------------------------------------------------------------ INSTAGRAM STORY (1080×1920)
def _story(brand, line_max, tr, example):
    d = (dict(tag="kısa konu etiketi", title="başlık satırları; son satır markanın vurgu renginde", body="tek fikir, 1-2 cümle; vurgu <b> içinde",
              cta="kısa eylem çağrısı, ok işareti koyma") if tr else
         dict(tag="short topic label", title="headline lines; the last line takes the brand accent colour", body="one idea in 1-2 sentences",
              cta="short call to action, no arrow"))
    return Series(brand, "story", "Instagram Story", {
        "tag": S(24, d["tag"]), "title": L(S(line_max, "satır" if tr else "line"), 2, 4, d["title"]),
        "body": S(150, d["body"], html=True), "cta": S(28, d["cta"])},
        lambda f: [("story", dict(f))], example, kind="story")

STORY = {
  "aba_psikoloji": _story("aba_psikoloji", 12, True, dict(tag="Sınav haftası", title=["Uykusuz", "gece", "işe", "yaramaz."],
      body="Son gece yeni konu değil, <b>dinlenmiş bir zihin</b> kazandırır. Bu akşam erken kapat.", cta="Birlikte planlayalım")),
  "aba_egitim": _story("aba_egitim", 14, True, dict(tag="IELTS hazırlık", title=["Hedef bant", "için plan", "şimdi başlar."],
      body="Dört bölüm, tek takvim. Hedef okulunun istediği puandan geriye doğru çalış.", cta="DM 'IELTS' yaz")),
  "e4i": _story("e4i", 13, False, dict(tag="Study tip", title=["Review", "after 1, 3", "and 7 days."],
      body="Spaced repetition beats cramming. Test yourself before you reread.", cta="Save this story")),
  "design_house": _story("design_house", 17, False, dict(tag="( Studio notes )", title=["Your first idea —", "is rarely", "your best one."],
      body="Keep it. Then make three more. The fourth one usually knows what it wants to be.", cta="DM “REVIEW”")),
}

# Platform → marka → seri listesi. Yeni platform eklemek için buraya bir giriş eklenir (bkz. agent/platforms.py).
PLATFORM_SERIES = {"instagram_feed": ALL, "instagram_story": {b: [s] for b, s in STORY.items()}}

def options(brand, platform="instagram_feed"):
    return PLATFORM_SERIES[platform][brand]
BRANDS = {"aba_psikoloji": "ABA Psikoloji", "aba_egitim": "ABA Eğitim", "e4i": "Education for Innovation", "design_house": "Design House Global"}

def get(brand, sid, platform=None):
    pools = [PLATFORM_SERIES[platform][brand]] if platform else [lst[brand] for lst in PLATFORM_SERIES.values()]
    for pool in pools:
        for s in pool:
            if s.id == sid: return s
    raise KeyError(f"{brand}/{sid}")
