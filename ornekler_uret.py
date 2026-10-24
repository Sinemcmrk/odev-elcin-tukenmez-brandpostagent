"""Örnek postları iki aşamalı akışla üretir → ornekler/ klasörü.
Her marka: 3 Instagram Feed + 1 Instagram Story (toplam 16).

Her örnekte: Agent 1 planı hazırlar → plan ekrana yazılır → SİZ onaylar, geri bildirim verir ya da atlarsınız
→ yalnızca onaylanan plan Agent 2'ye gider ve PNG üretilir. Onay atlanamaz.

Çalıştırma: python ornekler_uret.py   (Windows'ta: ornekler_uret.bat)
Yarıda kalırsa tekrar çalıştırın; tamamlanan örnekler atlanır.
"""
import json, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from agent.config import make_client, load_env
from agent.pipeline import ContentPlanner, VisualProducer, approve, slug, ApprovalError
from agent.llm import QuotaExceeded, LLMError
from agent import series as SR

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "ornekler"
FEED, STORY = "instagram_feed", "instagram_story"

# Her marka için 4 Feed + 1 Story. Feed konuları farklı içerik türlerindendir ve tasarımı Agent 1 OTOMATİK seçer.
# Örnek setinde aynı kompozisyon ikinci kez seçilirse agent'ın önerdiği farklı yerleşimli alternatife geçilir (çeşitlilik kontrolü).
# Biçim: (platform, konu)
TOPICS = {
    "aba_psikoloji": [(FEED, "Sınav kaygısı yaşayan öğrenciye kısa ve sakinleştirici bir mesaj"),
                      (FEED, "Çocuğu sınav sonucunu saklayan veliler için iletişim önerisi"),
                      (FEED, "Sınav dönemi hakkında doğru bilinen yanlışlar: mit ve gerçek"),
                      (FEED, "Pazartesi için küçük ve uygulanabilir bir haftalık çalışma rutini"),
                      (STORY, "Sınav sabahı için kısa bir nefes ve odak hatırlatması")],
    "aba_egitim": [(FEED, "ABD üniversite başvurusunda öğrencilerin sonradan 'keşke' dediği detaylar"),
                   (FEED, "IELTS hazırlık programımızın duyurusu"),
                   (FEED, "Başvuru dönemi başladı: öğrencileri son tarihlerini kontrol etmeye çağıran duyuru"),
                   (FEED, "Eğitim danışmanlığı: hedefe göre plan yapmanın önemi, kampanya mesajı"),
                   (STORY, "IELTS hazırlığına hedef puandan geriye doğru plan yaparak başlamak")],
    "e4i": [(FEED, "What is a hackathon and how does the process work, step by step"),
            (FEED, "Introducing climate tech as a future career field for high school students"),
            (FEED, "How to land your first internship: a 3-step playbook"),
            (FEED, "Innovation spotlight: robots that learn by watching humans"),
            (STORY, "Quick reminder for students: test yourself before you reread your notes")],
    "design_house": [(FEED, "One portfolio rule: why process pages matter more than the final piece"),
                     (FEED, "Editing your portfolio: fewer, stronger projects"),
                     (FEED, "The six creative disciplines students can apply for"),
                     (FEED, "Our portfolio direction service explained"),
                     (STORY, "Studio note: your first idea is rarely your best one")],
}


def show(plan):
    d, c = plan["design"], plan["content"]
    print(f"\n   ── PLAN v{plan['version']} · {plan['series_name']} · {d['format']} · {d['size']} · Görünüm: {d.get('theme')}")
    print(f"   Kompozisyon: {d.get('composition', '')}")
    if plan["analysis"].get("design_reason"): print(f"   Tasarım gerekçesi: {plan['analysis']['design_reason']}")
    print(f"   Niyet: {plan['analysis'].get('intent', '')}")
    print(f"   Gerekçe: {plan['analysis'].get('reason', '')}")
    for pg in d["pages"]:
        print(f"   [{pg['no']}] {pg['role']}: {pg['main_text']}")
    print("   Caption:\n      " + c["caption"].replace("\n", "\n      "))
    print("   " + " ".join(c["hashtags"]))
    if plan["checks"]["remaining_warnings"]:
        print("   ⚠ Uyarılar: " + " | ".join(plan["checks"]["remaining_warnings"]))


def decide(planner, plan):
    """Kullanıcı kararı: onay → onaylı plan, atla → None. Geri bildirim → yeni sürüm, tekrar sorulur."""
    while True:
        show(plan)
        try:
            ans = input("\n   [O] Onayla ve görseli üret · [G] Geri bildirim ver · [A] Atla  > ").strip().lower()
        except EOFError:
            return None
        if ans in ("o", "onayla", "e", "evet"):
            try:
                return approve(plan, by="kullanıcı (ornekler_uret)")
            except ApprovalError as e:
                print(f"   ⛔ {e}\n   Geri bildirim verin (G) ya da atlayın (A).")
                continue
        if ans in ("a", "atla"):
            return None
        if ans in ("g", "geri"):
            fb = input("   Geri bildiriminiz: ").strip()
            if fb:
                plan = planner.revise(plan, fb, on_step=lambda s, m, d=None: print(f"   [{s}] {m}"))


def summary():
    lines = ["# Agent ile üretilen örnek postlar", "",
             "Her örnek iki aşamayla üretildi: Agent 1 planı hazırladı, kullanıcı onayladı, Agent 2 PNG'yi üretti.", ""]
    for b in TOPICS:
        lines.append(f"## {SR.BRANDS[b]}")
        for pj in sorted((OUT / b).glob("*/post.json")):
            r = json.loads(pj.read_text(encoding="utf-8"))
            pl = json.loads((pj.parent / "plan_onayli.json").read_text(encoding="utf-8"))
            lines += [f"### {r['platform_name']} · {r['series_name']} — {r['topic']}", f"- Klasör: `{pj.parent.relative_to(ROOT)}`",
                      f"- Kompozisyon: {pl.get('composition', {}).get('desc', '')} · Görünüm: {pl.get('theme') or 'serinin kendi'}",
                      f"- Tasarım gerekçesi: {pl['analysis'].get('design_reason', '')}",
                      f"- Görseller: {len(r['images'])} PNG ({r['size'][0]}×{r['size'][1]}) · Model: {pl['model']} · {pl['llm_calls']} Gemini çağrısı",
                      f"- Niyet: {pl['analysis'].get('intent', '')}", f"- Seri gerekçesi: {pl['analysis'].get('reason', '')}",
                      f"- Plan sürümü: v{pl['version']} · geri bildirim: {len(pl['feedback_history'])} · onay: {pl['approval']['at']}",
                      f"- Kalan uyarı: {len(pl['checks']['remaining_warnings'])}", "",
                      "```", r["caption"], "", " ".join(r["hashtags"]), "```", ""]
    (OUT / "OZET.md").write_text("\n".join(lines), encoding="utf-8")


def _font(size=16):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(str(pathlib.Path(__file__).resolve().parent.parent / "templates" / "fonts" / "Montserrat.ttf") if __file__.endswith("cesitlilik_testi.py")
                                  else str(pathlib.Path(__file__).resolve().parent / "templates" / "fonts" / "Montserrat.ttf"), size)
    except Exception:
        return None


def contact_sheet():
    """Her markanın örneklerini yan yana gösteren karşılaştırma görseli (ilk sayfalar + seri/kompozisyon adı)."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    rows = []
    for b in TOPICS:
        items = []
        for pj in sorted((OUT / b).glob("*/post.json")):
            r = json.loads(pj.read_text(encoding="utf-8"))
            pl = json.loads((pj.parent / "plan_onayli.json").read_text(encoding="utf-8"))
            items.append((r["images"][0], f"{r['series_name']} · {pl.get('composition', {}).get('layout', '')}"))
        if items: rows.append((b, items))
    if not rows: return
    W, H, pad = 300, 375, 24
    sheet = Image.new("RGB", (pad + 5 * (W + pad), pad + len(rows) * (H + pad + 70)), "white")
    d = ImageDraw.Draw(sheet)
    for r, (b, items) in enumerate(rows):
        y = pad + r * (H + pad + 70)
        d.text((pad, y), SR.BRANDS[b] + "  (gerçek Gemini ile üretilen örnekler)", fill="black", font=_font())
        for c, (f, label) in enumerate(items[:5]):
            im = Image.open(f).convert("RGB"); im.thumbnail((W, H))
            sheet.paste(im, (pad + c * (W + pad), y + 22)); d.text((pad + c * (W + pad), y + 26 + H), label, fill="black", font=_font())
    sheet.save(OUT / "ozet.png")


def main():
    if not load_env()["api_key"]:
        sys.exit("GEMINI_API_KEY bulunamadı. Önce .env dosyasını oluşturun.")
    client, _ = make_client(log=lambda m: print("   ", m))
    print(f"Model: {client.model}\n")
    planner, producer = ContentPlanner(client, deep_review=load_env()["deep_review"]), VisualProducer()
    try:
        for b, topics in TOPICS.items():
            used = set()
            for i, (pf, t) in enumerate(topics, 1):
                done = list((OUT / b).glob(f"{i:02d}-*/post.json"))
                if done:
                    used.add(json.loads((done[0].parent / "plan_onayli.json").read_text(encoding="utf-8")).get("composition", {}).get("layout"))
                    print(f"✓ {SR.BRANDS[b]} #{i} zaten var, atlanıyor"); continue
                print(f"→ {SR.BRANDS[b]} #{i} ({'Story' if pf == STORY else 'Feed'}): {t}")
                step = lambda s, m, d=None: print(f"   [{s}] {m}")
                try:
                    r = planner.start(b, t, platform=pf, on_step=step)
                    if r["status"] == "needs_info":
                        answers = {q: input(f"   ? {q} (boş bırak = bilgi yok) > ").strip() for q in r["questions"]}
                        answers = {q: a for q, a in answers.items() if a}
                        r = planner.start(b, t, platform=pf, answers=answers or None, skip_questions=not answers, on_step=step)
                        if r["status"] == "needs_info":     # yanıt yetmediyse bilgi uydurmadan devam
                            r = planner.start(b, t, platform=pf, answers=answers or None, skip_questions=True, on_step=step)
                    plan = r["plan"]
                    lay = plan["composition"]["layout"]
                    if pf == FEED and lay in used:
                        alt = next((a for a in plan["alternatives"] if a["layout"] not in used), None)
                        if alt:
                            print(f"   ↺ '{plan['series_name']}' bu örnek setinde zaten kullanıldı; alternatif tasarıma geçiliyor: {alt['name']}")
                            plan = planner.switch_design(plan, alt["series"], on_step=step)
                    approved = decide(planner, plan)
                    if not approved:
                        print("   atlandı\n"); continue
                    used.add(approved["composition"]["layout"])
                    res = producer.produce(approved, OUT / b / f"{i:02d}-{slug(t, 40)}", on_step=step)
                    print(f"   ✓ {len(res['images'])} PNG\n")
                except QuotaExceeded:
                    raise
                except (LLMError, ValueError) as e:
                    print("   ✗ Hata:", e, "\n")
    except QuotaExceeded as e:
        print("\n⛔", e); print("Kota yenilendiğinde bu dosyayı tekrar çalıştırın; tamamlananlar atlanır.")
    summary(); contact_sheet()
    print("\nBitti. Sonuçlar: ornekler/OZET.md ve ornekler/ozet.png")


if __name__ == "__main__":
    main()
