"""Brand Post Agent — Streamlit arayüzü (iki aşamalı akış).
Çalıştırma: streamlit run app.py   (Windows'ta: baslat.bat)

Akış: ① Agent 1 planlar (gerekirse soru sorar) → ② Kullanıcı inceler, geri bildirim verir ya da onaylar → ③ Agent 2 PNG üretir.
"""
import io, json, pathlib, zipfile, tempfile
import streamlit as st
from agent import series as SR, platforms as PF, themes as TH
from agent.config import make_client, load_env
from agent.pipeline import ContentPlanner, VisualProducer, approve, ApprovalError
from agent.llm import LLMError, QuotaExceeded
from agent.validate import blocking

ROOT = pathlib.Path(__file__).resolve().parent
STEP_LABEL = {"analyze": "🧭 Niyet ve seri", "questions": "❓ Eksik bilgi", "write": "✍️ Metin", "check": "🔎 Brand Kit denetimi",
              "revise": "🛠️ Düzeltme", "feedback": "💬 Geri bildirim", "design": "📐 Tasarım planı", "render": "🎨 Görsel", "done": "✅ Tamamlandı"}
TYPE_LABEL = {"info": "Genel bilgilendirme", "event": "Etkinlik duyurusu", "achievement": "Başarı / sonuç duyurusu",
              "deadline": "Son tarih hatırlatması", "program": "Program tanıtımı"}

UI = ROOT / "templates" / "assets" / "ui"
ACCENT = {"aba_psikoloji": "#F48011", "aba_egitim": "#F95B1C", "e4i": "#774A9D", "design_house": "#902825"}
TAGLINE = {"aba_psikoloji": "Psikoloji · Türkçe", "aba_egitim": "Yurt dışı eğitim · Türkçe",
           "e4i": "İnovasyon vakfı · English", "design_house": "Sanat & tasarım portfolyo · English"}


def img64(path):
    import base64
    try:
        return "data:image/png;base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()
    except OSError:
        return ""


st.set_page_config(page_title="Brand Post Agent", page_icon=str(UI / "agent.png") if (UI / "agent.png").exists() else "🎨", layout="wide")
S = st.session_state
for k, v in {"stage": "input", "plan": None, "questions": None, "analysis": None, "result": None, "req": None, "calls": 0,
             "brand": "aba_psikoloji"}.items():
    S.setdefault(k, v)

def reset():
    S.stage, S.plan, S.questions, S.analysis, S.result = "input", None, None, None, None


def pick_brand(b):
    S.brand = b


accent = ACCENT.get(S.brand, "#E45823")
st.markdown(f"""<style>
:root{{--accent:{accent};--ink:#1B1E2B;--muted:#6B6B73;--line:#E7E3DC;--card:#FFFFFF}}
.block-container{{padding-top:1.4rem;max-width:1320px}}
.small{{color:var(--muted);font-size:.9rem}}
.hero{{display:flex;gap:22px;align-items:center;padding:22px 26px;border-radius:22px;margin-bottom:18px;color:#fff;
  background:radial-gradient(120% 140% at 100% 0%,{accent}55 0%,transparent 55%),linear-gradient(135deg,#1B1E2B 0%,#262A3B 100%)}}
.hero img{{width:76px;height:76px;border-radius:18px;box-shadow:0 8px 24px #0006}}
.hero h1{{font-size:2rem;margin:0;padding:0;color:#fff;letter-spacing:-.5px}}
.hero p{{margin:4px 0 10px;color:#D9DAE3;font-size:1rem}}
.pill{{display:inline-block;padding:5px 12px;border-radius:999px;background:#ffffff14;border:1px solid #ffffff26;color:#fff;
  font-size:.82rem;margin:0 6px 6px 0}}
.pill b{{color:{accent}}}
.bcard{{display:flex;gap:12px;align-items:center;padding:12px;border-radius:16px;background:var(--card);border:2px solid var(--line);
  margin-bottom:6px;transition:.15s}}
.bcard img{{width:54px;height:54px;border-radius:12px;flex:none}}
.bcard .n{{font-weight:700;color:var(--ink);line-height:1.15}}.bcard .t{{color:var(--muted);font-size:.8rem}}
.bcard.sel{{border-color:{accent};box-shadow:0 6px 18px {accent}33}}
.sec{{font-weight:700;color:var(--ink);font-size:1.05rem;margin:4px 0 8px}}
.sec span{{display:inline-block;width:24px;height:24px;border-radius:50%;background:{accent};color:#fff;text-align:center;
  line-height:24px;font-size:.8rem;margin-right:8px}}
.stepper{{display:flex;gap:8px;margin:4px 0 18px}}.stepper div{{flex:1;padding:10px 12px;border-radius:12px;background:#EFECE7;color:#77757A;font-size:.9rem}}
.stepper div.on{{background:{accent};color:#fff;font-weight:600}}.stepper div.ok{{background:#E5F3E8;color:#1D6B35}}
.sw{{display:inline-block;width:16px;height:16px;border-radius:4px;vertical-align:-3px;margin-right:6px;border:1px solid #0002}}
button[kind="primary"],[data-testid="stBaseButton-primary"]{{background:{accent}!important;border-color:{accent}!important;color:#fff!important}}
button[kind="primary"]:hover,[data-testid="stBaseButton-primary"]:hover{{filter:brightness(1.08)}}
[data-testid="stImage"] img{{border-radius:10px}}
.stTabs [aria-selected="true"]{{color:{accent}!important}}
.stTabs [data-baseweb="tab-highlight"]{{background:{accent}!important}}
</style>""", unsafe_allow_html=True)

# ------------------------------------------------------------------ yan panel
cfg = load_env()
with st.sidebar:
    st.markdown(f'<div style="display:flex;gap:10px;align-items:center;margin-bottom:6px"><img src="{img64(UI / "agent.png")}" '
                'style="width:40px;height:40px;border-radius:10px"><b style="font-size:1.1rem">Brand Post Agent</b></div>',
                unsafe_allow_html=True)
    st.header("⚙️ Ayarlar")
    if cfg["api_key"]:
        st.success("Gemini API anahtarı bulundu (.env)")
    else:
        st.error("GEMINI_API_KEY bulunamadı. .env dosyasını oluşturun (KURULUM_WINDOWS.md, adım 4).")
    st.caption(f"Model: **{cfg['model']}** (auto = ücretsiz Flash-Lite ailesinden otomatik seçim)")
    if st.button("Bağlantıyı test et", disabled=not cfg["api_key"]):
        try:
            c, _ = make_client(); st.success(f"Bağlantı başarılı. Kullanılacak model: {c.model}")
        except LLMError as e:
            st.error(str(e))
    deep = st.toggle("Ek marka denetimi (Gemini, +1 çağrı)", value=cfg["deep_review"])
    st.divider()
    st.markdown("**Ücretsiz katman**  \nAgent ücretli bir servise geçmez. Kota dolarsa bekler ya da açık bir mesajla durur. "
                "Bir plan genellikle 3–5 Gemini çağrısı kullanır; görsel üretimi (Agent 2) Gemini kullanmaz.")
    st.caption(f"Bu oturumda Gemini çağrısı: {S.calls}")

st.markdown(f"""<div class="hero"><img src="{img64(UI / 'agent.png')}" alt="">
<div><h1>Brand Post Agent</h1>
<p>Dört marka için Brand Kit'e sadık Instagram postları: konuyu yazın, planı inceleyin, onaylayın, görseli indirin.</p>
<span class="pill"><b>①</b> Agent 1 planlar ve tasarımı seçer</span><span class="pill"><b>②</b> Siz onaylarsınız</span>
<span class="pill"><b>③</b> Agent 2 görseli üretir</span><span class="pill">Gemini · ücretsiz katman</span>
<span class="pill">Feed 1080×1350 · Story 1080×1920</span></div></div>""", unsafe_allow_html=True)

tab_make, tab_examples, tab_how = st.tabs(["Post üret", "Örnek çıktılar", "Nasıl çalışır?"])

def planner():
    client, _ = make_client(log=lambda m: st.toast(m))
    return ContentPlanner(client, deep_review=deep), client

def status_cb(status):
    def cb(name, msg, data=None):
        status.write(f"**{STEP_LABEL.get(name, name)}** — {msg}")
        if name == "check" and data and data.get("issues"):
            for i in data["issues"][:6]: status.write(f"&nbsp;&nbsp;• {i}")
    return cb

def run_planner(**kw):
    status = st.status("Agent 1 çalışıyor…", expanded=True)
    try:
        pl, client = planner(); c0 = client.calls
        r = pl.start(**kw, on_step=status_cb(status))
        S.calls += client.calls - c0
        if r["status"] == "needs_info":
            S.stage, S.questions, S.analysis = "questions", r["questions"], r["analysis"]
            status.update(label="Agent 1 birkaç bilgi istiyor", state="complete", expanded=False)
        else:
            S.stage, S.plan = "review", r["plan"]
            status.update(label="Plan hazır · onayınızı bekliyor", state="complete", expanded=False)
        return True
    except QuotaExceeded as e:
        status.update(label="Kota sınırı", state="error"); st.error(str(e))
    except (LLMError, ValueError) as e:
        status.update(label="Durdu", state="error"); st.error(str(e))
    return False

# ------------------------------------------------------------------ POST ÜRET
with tab_make:
    st.markdown('<div class="sec"><span>1</span>Marka</div>', unsafe_allow_html=True)
    bcols = st.columns(len(SR.BRANDS))
    for k, b in enumerate(SR.BRANDS):
        with bcols[k]:
            sel = b == S.brand
            st.markdown(f'<div class="bcard{" sel" if sel else ""}"><img src="{img64(UI / (b + ".png"))}" alt="">'
                        f'<div><div class="n">{SR.BRANDS[b]}</div><div class="t">{TAGLINE.get(b, "")}</div></div></div>',
                        unsafe_allow_html=True)
            st.button(SR.BRANDS[b], key=f"brand_{b}", type="primary" if sel else "secondary", use_container_width=True,
                      on_click=pick_brand, args=(b,), disabled=S.stage != "input")
    left, right = st.columns([1, 1.7], gap="large")
    with left:
        locked = S.stage != "input"
        brand = S.brand
        pfs = PF.enabled()
        st.markdown('<div class="sec"><span>2</span>İçerik</div>', unsafe_allow_html=True)
        platform = st.radio("Platform", list(pfs), format_func=lambda p: pfs[p].name + (" (ana)" if p == PF.DEFAULT else ""),
                            horizontal=True, disabled=locked)
        st.caption(pfs[platform].note + "  \nLinkedIn: şirketin referanslarında yer almadığı için şimdilik kapalı; mimari eklenmeye hazır.")
        topic = st.text_area("Post konusu / isteğiniz", height=90, disabled=locked,
                             placeholder="ör. Sınav haftasında uyku hakkında yanlış bilinenler")
        facts = st.text_area("Doğrulanmış bilgi (isteğe bağlı)", height=70, disabled=locked,
                             placeholder="ör. 12 Kasım 2026 Pazar 14.00, Bebek ofisi, ücretsiz seminer",
                             help="Tarih, sayı, kabul sonucu gibi bilgiler yalnızca buraya yazıldığında kullanılır. Agent bilgi uydurmaz.")
        opts = ["auto"] + [s.id for s in SR.options(brand, platform)]
        def fmt(x):
            if x == "auto": return "🤖 Otomatik (Agent 1 seçsin)"
            s = SR.get(brand, x, platform)
            return (f"{s.name} — {SR.family(s)['desc'].split(':')[0]} · {dict(carousel='kaydırmalı', story='story').get(s.kind, 'tek post')}"
                    + (" · bilgi gerekir" if s.needs_facts else ""))
        sid = st.selectbox("Tasarım (kompozisyon)", opts, format_func=fmt, disabled=locked or platform != PF.DEFAULT,
                           help="Otomatik bırakırsanız Agent 1 konuya göre seçer ve 2–3 farklı alternatif önerir.")
        with st.expander("Fotoğraf ekle (isteğe bağlı)"):
            up = st.file_uploader("Arka plan fotoğrafı", type=["jpg", "jpeg", "png", "webp"], disabled=locked)
            op = st.slider("Fotoğraf görünürlüğü", 0.1, 0.8, 0.3, 0.05, disabled=locked)
        if S.stage == "input":
            if st.button("1 · Plan hazırla (Agent 1)", type="primary", disabled=not cfg["api_key"]):
                photo = None
                if up is not None:
                    tmp = pathlib.Path(tempfile.gettempdir()) / f"bpa_{up.name}"; tmp.write_bytes(up.getvalue()); photo = str(tmp)
                S.req = dict(brand=brand, topic=topic, platform=platform, facts=facts,
                             series_id=None if sid == "auto" or platform != PF.DEFAULT else sid, photo=photo, photo_opacity=op)
                with right:
                    ok = run_planner(**S.req)
                if ok: st.rerun()
        else:
            st.button("↺ Yeni post (baştan başla)", on_click=reset)

    with right:
        order = ["input", "questions", "review", "done"]
        cur = order.index(S.stage)
        labels = ["① İstek", "② Eksik bilgi", "③ Plan · onay", "④ Görsel (Agent 2)"]
        st.markdown('<div class="stepper">' + "".join(
            f'<div class="{"on" if k == cur else ("ok" if k < cur else "")}">{l}</div>' for k, l in enumerate(labels)) + "</div>",
            unsafe_allow_html=True)

        if S.stage == "input":
            st.info("Soldan marka, platform ve konuyu seçip **Plan hazırla**'ya basın. Agent 1 niyetinizi anlar, gerekirse kısa sorular sorar, "
                    "içerik ve tasarım planını hazırlar. **Görsel, siz onaylamadan üretilmez.**")

        # ---------------------------------------------------------- sorular
        if S.stage == "questions":
            a = S.analysis or {}
            st.subheader("Agent 1 birkaç bilgiye ihtiyaç duyuyor")
            st.caption(f"Anlaşılan niyet: {a.get('intent', '')} · Tür: {TYPE_LABEL.get(a.get('post_type'), a.get('post_type'))}")
            answers = {q: st.text_input(q, key=f"q{k}") for k, q in enumerate(S.questions)}
            c1, c2 = st.columns(2)
            if c1.button("Yanıtlarla devam et", type="primary"):
                if not any(v.strip() for v in answers.values()):
                    st.warning("En az bir soruyu yanıtlayın ya da bilgi vermeden devam edin.")
                else:
                    if run_planner(**S.req, answers={q: v for q, v in answers.items() if v.strip()}): st.rerun()
            if c2.button("Bilgi vermeden devam et", help="Agent eksik bilgiyi uydurmaz; postu bu bilgiler olmadan, genel bir dille yazar."):
                if run_planner(**S.req, skip_questions=True): st.rerun()

        # ---------------------------------------------------------- plan + onay
        if S.stage == "review" and S.plan:
            p, d = S.plan, S.plan["design"]
            a = p["analysis"]
            st.subheader(f"Plan v{p['version']} · {p['brand_name']} · {p['platform_name']}")
            st.markdown(f"**Niyet:** {a.get('intent', '')}  \n**Tür:** {TYPE_LABEL.get(a.get('post_type'), a.get('post_type'))} · "
                        f"**Seri:** {p['series_name']} · **Format:** {d['format']} · **Ölçü:** {d['size']}  \n"
                        f"**Seri gerekçesi:** {a.get('reason', '')}")
            if p.get("skipped_questions"):
                st.warning("Şu sorular yanıtlanmadan devam edildi; ilgili bilgi posta yazılmadı: " + " | ".join(p["skipped_questions"]))
            if p["feedback_history"] and p["feedback_history"][-1].get("model_note"):
                st.info("Agent 1 notu: " + p["feedback_history"][-1]["model_note"])

            st.markdown("#### İçerik")
            st.table([{"Sayfa": x["no"], "Rol": x["role"], "Ana metin": x["main_text"]} for x in d["pages"]])
            with st.expander("Tüm şablon alanları (başlık, içerik, CTA)", expanded=False):
                st.json(p["content"]["fields"])
            st.markdown("**Caption**")
            st.code(p["content"]["caption"] + "\n\n" + " ".join(p["content"]["hashtags"]), language=None)

            st.markdown("#### Tasarım planı")
            comp = p.get("composition") or {}
            c1, c2 = st.columns([1, 2.4])
            if comp.get("preview"): c1.image(comp["preview"], caption="Seçilen kompozisyon (örnek içerikle)")
            c2.markdown(f"**Kompozisyon:** {comp.get('desc', p['series_name'])}  \n"
                        + (f"**Neden bu tasarım:** {a.get('design_reason')}  \n" if a.get("design_reason") else "")
                        + (f"**Son kullanılanlar:** {', '.join(a.get('recent') or [])}" if a.get("recent") else ""))
            st.markdown("  \n".join([
                f"**Görünüm:** {d.get('theme', 'Serinin kendi görünümü')}",
                "**Renkler:** " + " ".join(f'<span class="sw" style="background:{c["hex"]}"></span>{c["name"]} `{c["hex"]}`' for c in d["colors"]),
                "**Fontlar:** " + " · ".join(d["fonts"]), f"**Logo:** {d['logo']}", f"**Fotoğraf:** {d['photo']}",
                f"**Yerleşim kontrolü:** {d['layout_check']}", f"🔒 {d['fixed_identity']}"]), unsafe_allow_html=True)
            if blocking(p["checks"]["remaining_warnings"]):
                st.error("Bu plan onaylanamaz: sizin vermediğiniz bir sayı / tarih içeriyor. Geri bildirimle düzeltin "
                         "(ör. 'Sayıyı 20 yap') ya da doğru bilgiyi yazıp yeniden planlayın.  \n" + " | ".join(blocking(p["checks"]["remaining_warnings"])))
            elif p["checks"]["remaining_warnings"]:
                st.warning("Kalan uyarılar: " + " | ".join(p["checks"]["remaining_warnings"]))
            else:
                st.success("Plan tüm Brand Kit kontrollerinden geçti.")

            alts = p.get("alternatives") or []
            if alts:
                st.markdown("#### Başka tasarım dene")
                st.caption("Aynı konu, farklı kompozisyon. Seçince Agent 1 metni yeni tasarıma göre yeniden yazar (1 Gemini çağrısı).")
                cols = st.columns(len(alts))
                for k, alt in enumerate(alts):
                    with cols[k]:
                        if alt.get("preview"): st.image(alt["preview"])
                        st.markdown(f"**{alt['name']}**  \n<span class='small'>{alt['desc']}</span>", unsafe_allow_html=True)
                        if st.button("Bu tasarımı dene", key=f"alt{k}v{p['version']}"):
                            status = st.status(f"Agent 1 '{alt['name']}' tasarımını hazırlıyor…", expanded=True)
                            try:
                                pl, client = planner(); c0 = client.calls
                                S.plan = pl.switch_design(p, alt["series"], on_step=status_cb(status)); S.calls += client.calls - c0
                                status.update(label=f"Plan v{S.plan['version']} hazır", state="complete"); st.rerun()
                            except (LLMError, ValueError) as e:
                                status.update(label="Durdu", state="error"); st.error(str(e))

            th_opts = TH.options(p["brand"])
            if th_opts and TH.themable(p["brand"], SR.get(p["brand"], p["series"], p["platform"])):
                keys = list(th_opts)
                cur = keys.index(p["theme"]) if p.get("theme") in keys else 0
                c1, c2 = st.columns([2, 1])
                new_th = c1.selectbox("Görünümü değiştir (Brand Kit renkleri içinde)", keys, index=cur, format_func=lambda k: th_opts[k],
                                      key=f"th{p['version']}")
                if c2.button("Görünümü uygula", disabled=new_th == p.get("theme")):
                    S.plan = ContentPlanner(None, deep_review=False).edit(p, theme=new_th); st.rerun()

            st.divider()
            st.markdown("#### Kararınız")
            fb = st.text_area("Geri bildirim / değişiklik isteği", placeholder="ör. Başlık daha kısa olsun · Bunu infografik yap · Carousel olarak anlat · Daha minimal bir tasarım", key=f"fb{p['version']}")
            c1, c2 = st.columns(2)
            if c1.button("💬 Geri bildirimi uygula (Agent 1)", disabled=not fb.strip()):
                status = st.status("Agent 1 planı güncelliyor…", expanded=True)
                try:
                    pl, client = planner(); c0 = client.calls
                    S.plan = pl.revise(p, fb, on_step=status_cb(status)); S.calls += client.calls - c0
                    status.update(label=f"Plan v{S.plan['version']} hazır", state="complete"); st.rerun()
                except (LLMError, ValueError) as e:
                    status.update(label="Durdu", state="error"); st.error(str(e))
            if c2.button("✅ Onayla ve görseli üret (Agent 2)", type="primary"):
                status = st.status("Agent 2 görseli üretiyor…", expanded=True)
                try:
                    approved = approve(p, by="kullanıcı (arayüz)")
                    S.result = VisualProducer().produce(approved, on_step=status_cb(status))
                    S.plan, S.stage = approved, "done"
                    status.update(label="Görsel hazır", state="complete"); st.rerun()
                except (ApprovalError, RuntimeError, ValueError) as e:
                    status.update(label="Durdu", state="error"); st.error(str(e))
            with st.expander("✏️ Metni elle düzenle (Gemini kullanmaz)"):
                cap = st.text_area("Caption", p["content"]["caption"], height=160, key=f"cap{p['version']}")
                tags = st.text_input("Hashtag'ler (boşlukla)", " ".join(p["content"]["hashtags"]), key=f"tag{p['version']}")
                fj = st.text_area("Şablon alanları (JSON)", json.dumps(p["content"]["fields"], ensure_ascii=False, indent=1), height=220,
                                  key=f"fj{p['version']}", help="Yalnızca metinleri değiştirin; logo, renk ve font şablonda sabittir.")
                if st.button("Düzenlemeyi kaydet (yeni plan sürümü)"):
                    try:
                        S.plan = ContentPlanner(None, deep_review=False).edit(p, json.loads(fj), cap, tags.split()); st.rerun()
                    except json.JSONDecodeError as e:
                        st.error(f"JSON hatalı: {e}")
            st.download_button("Plan JSON'u indir", json.dumps(p, ensure_ascii=False, indent=2), file_name=f"plan-{p['plan_id']}-v{p['version']}.json",
                               mime="application/json")

        # ---------------------------------------------------------- sonuç
        if S.stage == "done" and S.result:
            res = S.result
            st.subheader(f"{res['series_name']} · {res['platform_name']}")
            st.caption(f"Onaylanan plan v{res['plan_version']} · onay: {res['approved_at']} · {len(res['images'])} PNG · {res['seconds']} sn")
            imgs = res["images"]
            cols = st.columns(min(len(imgs), 4))
            for k, pth in enumerate(imgs):
                with cols[k % len(cols)]:
                    st.image(pth, caption=f"Sayfa {k + 1}" if len(imgs) > 1 else None)
                    st.download_button("PNG indir", open(pth, "rb").read(), file_name=pathlib.Path(pth).name, mime="image/png", key=f"dl{k}")
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as z:
                for pth in imgs: z.write(pth, pathlib.Path(pth).name)
                z.writestr("caption.txt", res["caption"] + "\n\n" + " ".join(res["hashtags"]))
                z.writestr("plan_onayli.json", json.dumps(S.plan, ensure_ascii=False, indent=2))
            st.download_button("⬇️ Tümünü indir (PNG + caption + plan, ZIP)", buf.getvalue(),
                               file_name=f"{pathlib.Path(res['out_dir']).name}.zip", mime="application/zip")
            st.code(res["caption"] + "\n\n" + " ".join(res["hashtags"]), language=None)

# ------------------------------------------------------------------ ÖRNEKLER
with tab_examples:
    posts = sorted((ROOT / "ornekler").glob("*/*/post.json"))
    if not posts:
        st.info("Henüz örnek yok. `ornekler_uret.bat` dosyasını çalıştırarak örnek postları üretin.")
    for b in SR.BRANDS:
        items = [x for x in posts if x.parent.parent.name == b]
        if not items: continue
        st.markdown(f"### {SR.BRANDS[b]}")
        for pj in items:
            r = json.loads(pj.read_text(encoding="utf-8"))
            with st.expander(f"{r.get('platform_name', 'Instagram Feed')} · {r['series_name']} — {r['topic']}"):
                pngs = sorted(pj.parent.glob("*.png"))
                cols = st.columns(min(len(pngs), 4) or 1)
                for k, x in enumerate(pngs): cols[k % len(cols)].image(str(x))
                st.code(r["caption"] + "\n\n" + " ".join(r["hashtags"]), language=None)

# ------------------------------------------------------------------ NASIL ÇALIŞIR
with tab_how:
    st.markdown("""
**Agent 1 — Content & Design Planner** (Gemini, ücretsiz katman)
1. Marka, platform ve konuyu analiz eder; niyeti ve post türünü belirler.
2. Yalnızca gerçekten gerekliyse soru sorar: etkinlikte tarih/saat/yer, başarı duyurusunda doğrulanmış sonuç, son tarih hatırlatmasında tarih.
   Genel bilgilendirici postlarda soru sormaz.
3. Brand Kit ve Post Kütüphanesi kurallarıyla seriyi seçer; başlık, içerik, CTA, caption ve hashtag'leri yazar.
4. Kod tabanlı Brand Kit denetimi (karakter sınırı, uydurma sayı/tarih, yasaklı vaat, dil, hashtag) ve metnin şablona sığdığının
   ölçümü (PNG üretmeden). Sorun varsa en fazla 2 tur düzeltir.
5. Kısa bir tasarım planı hazırlar: format, sayfa sayısı, sayfa rolleri, renkler, fontlar, logo yeri.

**Kullanıcı onayı** — Plan size gösterilir. Geri bildirim verebilir, metni elle düzenleyebilir ya da onaylayabilirsiniz.
Onay, planın içeriğine bağlı bir parmak izidir (SHA-256): onaydan sonra plan değişirse Agent 2 üretmeyi reddeder.

**Agent 2 — Visual Production Agent** (LLM kullanmaz)
Onaylanan plan JSON'unu alır, Post Kütüphanesinin HTML/CSS şablonlarıyla Playwright üzerinden PNG üretir; carousel'de tüm sayfaları.
Logo, renk, font ve yerleşim şablonda sabittir; plan yalnızca metin taşır.

**Platformlar:** Instagram Feed 1080×1350 (ana) · Instagram Story 1080×1920 (her marka için bir düzen) · LinkedIn: planlandı (`agent/platforms.py`).
""")
