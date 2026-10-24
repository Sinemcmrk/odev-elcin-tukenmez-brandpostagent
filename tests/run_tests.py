"""Çevrimdışı testler. Gemini yerine sahte sunucu kullanır; gerçek API anahtarı gerekmez.
Çalıştırma:  python -m tests.run_tests
"""
import sys, json, pathlib, shutil, traceback
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tests import mock_gemini as MG
from agent import series as SR, validate as V
from agent.llm import GeminiClient, QuotaExceeded, LLMError
from agent.pipeline import ContentPlanner, VisualProducer, approve, ApprovalError
from agent import platforms as PF
from agent.render import render_pages
from PIL import Image
import subprocess

OUT = ROOT / "tests" / "test_ciktilari"
results = []

def test(name):
    def deco(fn):
        try:
            fn(); results.append((name, True, "")); print("✓", name)
        except Exception as e:
            results.append((name, False, f"{type(e).__name__}: {e}")); print("✗", name); traceback.print_exc()
        return fn
    return deco

srv = MG.start(8765)
BASE = "http://127.0.0.1:8765"
def client(**kw): return GeminiClient("TEST-KEY", "auto", BASE, min_interval=0, **kw)

@test("Doğrulama: uydurma yüzde ve büyük sayı yakalanır")
def _():
    iss = V.check_facts("Öğrencilerin %87'si 3 haftada 250 puan artırdı.", "")
    assert len(iss) == 2, iss

@test("Doğrulama: kullanıcının verdiği sayı serbest")
def _():
    assert V.check_facts("Bu yıl 221 öğrenci kabul aldı.", "221 öğrenci kabul") == []

@test("Doğrulama: uydurma tarih yakalanır")
def _():
    assert V.check_facts("Son başvuru 15 Kasım.", "") != []

@test("Doğrulama: karakter sınırı ve liste sayısı")
def _():
    s = SR.get("aba_psikoloji", "ic_ses")
    f = dict(s.example, quote=["tek"], body="x" * 200)
    _, iss = V.check_schema(s.schema, f)
    assert any("öğe" in i for i in iss) and any("karakter" in i for i in iss), iss

@test("Doğrulama: HTML temizleme (yalnızca izinli etiketler)")
def _():
    out = V.sanitize("<script>alert(1)</script><b>ok</b><br>", True)
    assert "<script>" not in out and "<b>ok</b>" in out and "<br>" in out

@test("Doğrulama: marka hashtag'i başa alınır, İngilizce kontrolü")
def _():
    s = SR.get("e4i", "study")
    _, cap, tags, iss, fixes = V.check_post("e4i", "en", s, s.example, "Çalışma ipucu", ["#a", "#b"], "", "", [])
    assert tags[0] == "#E4I" and fixes and any("İngilizce" in i for i in iss) and any("hashtag" in i for i in iss)

@test("Model seçimi: ücretsiz Flash-Lite tercih edilir, Pro/embedding seçilmez")
def _():
    c = client(); assert c.model == "gemini-3.5-flash-lite", c.model
    assert all("pro" not in m and "embedding" not in m for m in c.candidates), c.candidates

@test("Geçersiz API anahtarı anlaşılır hata verir")
def _():
    try:
        GeminiClient("YANLIS", "auto", BASE, min_interval=0); raise AssertionError("hata bekleniyordu")
    except LLMError as e:
        assert "geçersiz" in str(e)

@test("Dakikalık kota (429): bekleyip tekrar dener")
def _():
    MG.STATE.update(calls=0, fail_first_429=True)
    c = client(); r = c.generate_json("Sen markanın Brand Kit denetçisisin.", "x")
    MG.STATE["fail_first_429"] = False
    assert r["score"] == 9 and c.calls == 2

@test("Günlük kota: başka ücretsiz modele geçer, hepsi doluysa açıkça durur")
def _():
    MG.STATE.update(calls=0, daily_quota=True, log=[])
    c = client()
    try:
        c.generate_json("Sen markanın Brand Kit denetçisisin.", "x"); raise AssertionError("kota hatası bekleniyordu")
    except QuotaExceeded as e:
        assert "kota" in str(e).lower()
    finally:
        MG.STATE["daily_quota"] = False
    assert len(c.candidates) == 1  # aday listesi tükendi, ücretli servise geçilmedi

@test("Tüm şablonlar örnek içerikle taşmadan çizilir (32 Feed serisi + 4 Story)")
def _():
    for pf, by_brand in SR.PLATFORM_SERIES.items():
        for b, lst in by_brand.items():
            for s in lst:
                pages = [(f"{pf}-{s.id}-{k+1}", t, d) for k, (t, d) in enumerate(s.build(s.example))]
                pngs, ov = render_pages(b, pages, OUT / "seri_ornekleri" / b)
                assert not any(ov.values()), (b, s.id, ov)
                size = (1080, 1920) if pf == "instagram_story" else (1080, 1350)
                assert all(Image.open(p).size == size for p in pngs), (b, s.id)

WORK = OUT / "agent"
def planner(**kw):
    MG.STATE.update(calls=0, faulty_first_write=kw.pop("faulty", True))
    return ContentPlanner(client(), work_root=WORK, **kw)
def pngs_under(path): return list(pathlib.Path(path).rglob("*.png"))
def produce(plan, name):
    return VisualProducer(WORK).produce(approve(plan, by="test"), WORK / name)

@test("Agent 1 · niyet: genel bilgilendirici postta gereksiz soru sorulmaz, niyet ve tür belirlenir")
def _():
    r = planner().start("aba_psikoloji", "Sınav öncesi uyku hakkında yanlış bilinenler")
    assert r["status"] == "ready", r.get("questions")
    a = r["plan"]["analysis"]
    assert a["post_type"] == "info" and a["intent"] and r["plan"]["series"] == "mit"

@test("Agent 1 · soru: etkinlik duyurusunda tarih yoksa sorar, plan ve görsel üretmez")
def _():
    shutil.rmtree(WORK / "_olcum", ignore_errors=True)
    before = len(pngs_under(WORK))
    r = planner().start("aba_egitim", "Bebek ofisimizde ücretsiz IELTS semineri düzenliyoruz")
    assert r["status"] == "needs_info" and any("tarih" in q.lower() for q in r["questions"]), r
    assert "plan" not in r and len(pngs_under(WORK)) == before

@test("Agent 1 · soru: yanıt verilince plan hazırlanır, tarih yanıttan alınır ve tekrar sorulmaz")
def _():
    q = "Etkinliğin tarihi, saati ve yeri (ya da çevrim içi bilgisi) nedir?"
    r = planner(faulty=False).start("aba_egitim", "Bebek ofisimizde ücretsiz IELTS semineri düzenliyoruz",
                                    answers={q: "12 Kasım 2026 Pazar 14.00, Bebek ofisi"})
    assert r["status"] == "ready" and "12 Kasım 2026" in r["plan"]["facts"]

@test("Agent 1 · soru: başarı duyurusu doğrulanmış bilgi olmadan yazılmaz, bilgiyle Kabul Duyurusu hazırlanır")
def _():
    r = planner().start("aba_egitim", "Bu yılki kabul sonuçlarımız", series_id="kabul")
    assert r["status"] == "needs_info" and r["blocking"]
    try:
        planner().start("aba_egitim", "Bu yılki kabul sonuçlarımız", series_id="kabul", skip_questions=True); raise AssertionError("hata bekleniyordu")
    except ValueError as e:
        assert "doğrulanmış" in str(e).lower()
    r = planner(faulty=False).start("aba_egitim", "Bu yılki kabul sonuçlarımız", series_id="kabul",
                                    facts="Bu yıl 221 öğrenci Oxford, Cambridge, Imperial, LSE ve UCL'den kabul aldı")
    assert r["status"] == "ready" and r["plan"]["series"] == "kabul" and not r["plan"]["checks"]["remaining_warnings"]

@test("Başarı duyurusu: kullanıcı '20 öğrenci' derse markanın geçmiş sonucu (221) ve verilmeyen okullar kullanılamaz")
def _():
    from agent import prompts as PR
    ser = SR.get("aba_egitim", "kabul")
    assert "221" not in PR.example_for(ser) and "OXFORD" not in PR.example_for(ser)
    q = "Paylaşılacak doğrulanmış sonuç nedir? (ör. kaç öğrenci, hangi okullar; paylaşım izni var mı?)"
    r = planner(faulty=False).start("aba_egitim", "Bu yılki kabul sonuçlarımız", series_id="kabul", answers={q: "20 öğrenci, Oxford"})
    p = r["plan"]   # sahte model kütüphane örneğini (221, beş okul) kopyalıyor
    assert p["content"]["fields"]["schools"] == ["OXFORD"]
    assert any("221" in w for w in p["checks"]["remaining_warnings"])
    try:
        approve(p); raise AssertionError("uydurma sayı içeren plan onaylanmamalı")
    except ApprovalError as e:
        assert "onaylanamaz" in str(e)

@test("Kopya ve okul denetimi: kütüphane örneğinin cümleleri kopyalanamaz, Design House listesinde olmayan okul yazılamaz")
def _():
    s = SR.get("e4i", "field")
    assert any("kütüphane örneğiyle aynı" in i for i in V.check_copy(s, s.example))
    d = SR.get("design_house", "destinations"); kb = json.loads((ROOT / "knowledge" / "design_house.json").read_text(encoding="utf-8"))
    assert V.check_schools(d, d.example, kb["verified_facts"]) == []
    bad = json.loads(json.dumps(d.example)); bad["cities"][0]["schools"] = "Harvard<br>+ RCA."
    assert any("Harvard" in i for i in V.check_schools(d, bad, kb["verified_facts"]))

@test("Agent 1 · plan: içerik + tasarım planı sunulur, denetim/düzeltme çalışır, Agent 1 PNG üretmez")
def _():
    before = len(pngs_under(WORK))
    p = planner().start("aba_psikoloji", "Sınav öncesi uyku hakkında yanlış bilinenler")["plan"]
    d = p["design"]
    assert d["format"] == "Carousel · 4 sayfa" and len(d["pages"]) == 4 and d["size"] == "1080×1350"
    assert d["colors"] and d["fonts"] and d["logo"] and d["fixed_identity"]
    assert p["content"]["caption"] and p["content"]["hashtags"][0] == "#ABAPsikoloji"
    first = p["checks"]["rounds"][0]["issues"]
    assert any("Doğrulanmamış" in i for i in first) and len(p["checks"]["rounds"]) >= 2 and not p["checks"]["remaining_warnings"]
    assert p["approval"] == {"status": "pending"} and len(pngs_under(WORK)) == before
    json.dumps(p)  # plan JSON'a çevrilebilir olmalı

@test("Kullanıcı geri bildirimi: yeni plan sürümü, onay sıfırlanır, marka dışı istek (logo rengi) uygulanmaz")
def _():
    pl = planner()
    p = pl.start("aba_psikoloji", "Sınav öncesi uyku hakkında yanlış bilinenler")["plan"]
    p2 = pl.revise(approve(p), "CTA daha samimi olsun, logo da yeşil olsun")
    assert p2["version"] == 2 and p2["approval"]["status"] == "pending"
    assert p2["content"]["caption"] != p["content"]["caption"] and p2["feedback_history"][-1]["text"].startswith("CTA")
    assert "Logo" in p2["feedback_history"][-1]["model_note"]

@test("Elle düzenleme: Gemini çağrısı olmadan yeni sürüm, kod denetimi yine çalışır")
def _():
    pl = planner(faulty=False)
    p = pl.start("design_house", "One studio note about first ideas", series_id="statement")["plan"]
    c0 = pl.llm.calls
    p2 = pl.edit(p, caption="New caption about first ideas.\n\nKeep going.")
    assert pl.llm.calls == c0 and p2["version"] == 2 and p2["approval"]["status"] == "pending"
    p3 = pl.edit(p2, caption="Öğrenciler için 87% başarı")
    assert any("İngilizce" in w or "Doğrulanmamış" in w for w in p3["checks"]["remaining_warnings"])

@test("Onay kapısı: onaysız plan ve onaydan sonra değiştirilmiş plan Agent 2 tarafından reddedilir")
def _():
    p = planner(faulty=False).start("e4i", "How to prepare for a hackathon", series_id="playbook")["plan"]
    for bad in (p, dict(approve(p), content=dict(p["content"], caption="changed after approval"))):
        try:
            VisualProducer(WORK).produce(bad, WORK / "red"); raise AssertionError("üretim reddedilmeliydi")
        except ApprovalError:
            pass
    assert not (WORK / "red").exists()
    pf = OUT / "onaysiz_plan.json"; pf.write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "agent.producer", str(pf)], cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8")
    assert r.returncode != 0 and "reddedildi" in (r.stderr + r.stdout)

@test("Agent 2: onay sonrası carousel'in tüm sayfaları PNG olarak üretilir, caption ve onaylı plan kaydedilir")
def _():
    p = planner(faulty=False).start("e4i", "How to prepare for a hackathon", series_id="playbook")["plan"]
    r = produce(p, "e4i-playbook")
    out = pathlib.Path(r["out_dir"])
    assert len(r["images"]) == 4 and all(Image.open(x).size == (1080, 1350) for x in r["images"])
    assert (out / "caption.txt").exists() and json.loads((out / "plan_onayli.json").read_text(encoding="utf-8"))["approval"]["status"] == "approved"

@test("Dört marka · Instagram Feed: plan → onay → PNG (1080×1350)")
def _():
    topics = {"aba_psikoloji": "Bölüm seçerken yaşanan kararsızlık", "aba_egitim": "ABD başvurusunda keşke denen detaylar",
              "e4i": "A study tip against procrastination", "design_house": "Why process pages matter in a portfolio"}
    for b, t in topics.items():
        r = planner().start(b, t)
        assert r["status"] == "ready", (b, r.get("questions"))
        res = produce(r["plan"], f"feed-{b}")
        assert res["images"] and all(Image.open(x).size == (1080, 1350) for x in res["images"]), b
        assert res["hashtags"][0] == V.BRAND_TAG[b]

@test("Dört marka · Instagram Story: plan → onay → PNG (1080×1920)")
def _():
    for b in SR.BRANDS:
        r = planner().start(b, "Kısa bir motivasyon hatırlatması" if b.startswith("aba") else "A short motivation reminder", platform="instagram_story")
        p = r["plan"]
        assert r["status"] == "ready" and p["series"] == "story" and p["design"]["size"] == "1080×1920", b
        assert 1 <= len(p["content"]["hashtags"]) <= 3
        res = produce(p, f"story-{b}")
        assert len(res["images"]) == 1 and Image.open(res["images"][0]).size == (1080, 1920), b

@test("Marka kimliği kilidi: plana eklenen stil/HTML üretimde etkisiz kalır")
def _():
    p = planner(faulty=False).start("aba_psikoloji", "Kendini kıyaslama", series_id="ic_ses")["plan"]
    p["content"]["fields"]["label"] = "<span style='color:#00ff00'>Yeşil</span>"
    r = produce(p, "kimlik")
    assert "&lt;span" in r["fields"]["label"] and "<span style" not in json.dumps(r["fields"])

@test("Gemini yanıtı listeye sarılı gelirse ([{...}]) agent yine çalışır")
def _():
    from agent.llm import parse_json
    assert parse_json('[{"a": 1}]') == {"a": 1} and parse_json('```json\n{"a": 2}\n```') == {"a": 2}
    MG.STATE["wrap_list"] = True
    try:
        r = planner(faulty=False).start("aba_egitim", "Bu yılki kabul sonuçlarımız", series_id="kabul",
                                        facts="Bu yıl 221 öğrenci Oxford, Cambridge, Imperial, LSE ve UCL'den kabul aldı")
    finally:
        MG.STATE["wrap_list"] = False
    assert r["status"] == "ready" and r["plan"]["content"]["fields"]

@test("Görünüm temaları: her plan bir tema alır, tema değişikliği yeni sürüm açar, PNG'nin zemini temaya göre değişir")
def _():
    from agent import themes as TH
    for b in SR.BRANDS:
        assert len(TH.options(b)) >= 3, b
    pl = planner(faulty=False)
    p = pl.start("aba_psikoloji", "Kendini kıyaslama", series_id="ic_ses", theme="krem")["plan"]
    assert p["theme"] == "krem" and p["design"]["theme"] == "Krem zemin"
    p2 = pl.edit(approve(p), theme="koyu")
    assert p2["version"] == 2 and p2["theme"] == "koyu" and p2["approval"]["status"] == "pending"
    light = Image.open(produce(p, "tema-krem")["images"][0]).convert("RGB").getpixel((540, 1200))
    dark = Image.open(produce(p2, "tema-koyu")["images"][0]).convert("RGB").getpixel((540, 1200))
    assert sum(light) > 600 and sum(dark) < 200, (light, dark)
    u = pl.start("aba_psikoloji", "Tercih döneminde aile içi konuşmalar", series_id="uzman")["plan"]
    assert u["theme"] is None   # uzman serisi kendi düzenini korur

@test("Telefon numarası uydurma sayı sayılmaz (+90 212 287 86 06)")
def _():
    assert V.check_facts("Bize yazın: +90 212 287 86 06 · +90 (545) 359 66 36", "") == []

@test("Kütüphane–kod tutarlılığı: PDF'deki her seri agent'ta var, agent'taki her seri PDF'de belgeli")
def _():
    import importlib
    from agent.prompts import META_ID
    sys.path.insert(0, str(ROOT / "templates")); sys.path.insert(0, str(ROOT / "templates" / "brands"))
    for b in SR.BRANDS:
        lib = {x["id"] for x in importlib.import_module(b).META["series"]}
        code = {("06" if s.id == "uzman" else META_ID[s.id]) for s in SR.ALL[b]} | {"09"}
        assert lib == code, (b, lib ^ code)
        assert len(SR.ALL[b]) == 8 and len({SR.family(x)["layout"] for x in SR.ALL[b]}) == 8, b
        for x in SR.ALL[b] + [SR.STORY[b]]:
            assert (ROOT / "templates" / "previews" / b / f"{x.id}.png").exists(), (b, x.id)

@test("Tasarım seçimi: alternatifler farklı yerleşimde, son kullanılan kompozisyon geride kalır, geçmiş kaydedilir")
def _():
    from agent import design as DS
    DS.HISTORY = OUT / "gecmis.json"; DS.HISTORY.unlink(missing_ok=True)
    pl = planner(faulty=False)
    p = pl.start("e4i", "What is a hackathon and how does the process work, step by step")["plan"]
    lays = [p["composition"]["layout"]] + [a["layout"] for a in p["alternatives"]]
    assert len(p["alternatives"]) >= 2 and len(set(lays)) == len(lays), lays
    produce(p, "gecmis")
    assert DS.recent("e4i")[0]["series"] == p["series"]
    ranked = DS.rank("e4i", SR.ALL["e4i"], "generic topic", "info", history=DS.recent("e4i"))
    assert ranked[0].id != p["series"]       # eşit uygunlukta son kullanılan kompozisyon öne çıkmaz

@test("Başka tasarım: 'Bu tasarımı dene' ve 'infografik yap' geri bildirimi gerçekten farklı şablona geçer")
def _():
    pl = planner(faulty=False)
    p = pl.start("aba_egitim", "Eğitim danışmanlığı: hedefe göre plan yapmanın önemi")["plan"]
    alt = p["alternatives"][0]
    p2 = pl.switch_design(p, alt["series"])
    assert p2["series"] == alt["series"] != p["series"] and p2["version"] == 2 and p2["approval"]["status"] == "pending"
    assert p2["composition"]["layout"] != p["composition"]["layout"]
    q = pl.start("e4i", "Climate tech as a future career", series_id="field")["plan"]
    q2 = pl.revise(q, "Bunu infografik yap")
    assert q2["series"] == "process" and q2["feedback_history"][-1]["type"] == "design"
    r = produce(q2, "infografik"); assert Image.open(r["images"][0]).size == (1080, 1350)

@test("Fotoğraf yuvası: fotoğraf yüklenince tasarımın parçası olur, yüklenmezse grafik yedek kullanılır")
def _():
    ph = OUT / "foto_mavi.png"; Image.new("RGB", (900, 900), (20, 90, 200)).save(ph)
    pl = planner(faulty=False)
    with_p = produce(pl.start("e4i", "Robots that learn", series_id="spotlight", photo=str(ph), photo_opacity=1)["plan"], "slot-foto")
    no_p = produce(pl.start("e4i", "Robots that learn", series_id="spotlight")["plan"], "slot-yok")
    a = Image.open(with_p["images"][0]).convert("RGB").getpixel((540, 300)); b = Image.open(no_p["images"][0]).convert("RGB").getpixel((540, 300))
    assert a[2] > 150 and a[0] < 80 and a != b, (a, b)

@test("Metin iki kez kaçırılmaz (& işareti görselde &amp; olarak çıkmaz)")
def _():
    assert V.sanitize(V.sanitize("art & design", False), False) == "art &amp; design"

@test("Platformlar: Instagram Feed ana, Story ikincil, LinkedIn kayıtlı ama kapalı")
def _():
    assert PF.DEFAULT == "instagram_feed" and set(PF.enabled()) == {"instagram_feed", "instagram_story"}
    try:
        PF.get("linkedin"); raise AssertionError("LinkedIn kapalı olmalı")
    except ValueError:
        pass
    assert [s.id for s in SR.options("e4i", "instagram_story")] == ["story"] and len(SR.options("e4i")) == 8

@test("Fotoğraf katmanı ile üretim")
def _():
    ph = OUT / "foto.png"; Image.new("RGB", (800, 1000), (120, 90, 60)).save(ph)
    r = planner(faulty=False).start("design_house", "first idea", series_id="statement", photo=str(ph), photo_opacity=0.4)
    assert "fotoğraf" in r["plan"]["design"]["photo"].lower()
    assert len(produce(r["plan"], "foto")["images"]) == 1

if __name__ == "__main__":
    ok = sum(1 for _, s, _ in results if s)
    print(f"\n{ok}/{len(results)} test geçti")
    (ROOT / "tests" / "test_sonuclari.json").write_text(json.dumps([{"test": n, "gecti": s, "hata": e} for n, s, e in results], ensure_ascii=False, indent=1), encoding="utf-8")
    srv.shutdown()
    sys.exit(0 if ok == len(results) else 1)
