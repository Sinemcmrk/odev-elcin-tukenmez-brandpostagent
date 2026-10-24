"""Tasarım çeşitliliği testi (SAHTE Gemini ile).

Her marka için ornekler_uret.py'deki 4 Feed konusu, gerçek akışla (Agent 1 otomatik tasarım seçimi → onay → Agent 2) üretilir.
Gemini yerine tests/mock_gemini.py kullanılır: metinler kütüphane örneklerinden türetilir, tasarım seçimini kelime
örtüşmesine bakan basit bir "model" yapar. Bu yüzden çıktılar GERÇEK AGENT ÇIKTISI DEĞİLDİR; test edilen şey
tasarım seçimi, çeşitlilik kontrolü ve şablonların gerçekten farklı yerleşimler üretmesidir.

Kontroller:
  1. Her markanın 4 postu 4 farklı kompozisyon ailesinden (layout) gelir.
  2. Yerleşim farkı ölçülür: görsellerin kenar haritaları (yalnızca şekil, renk değil) karşılaştırılır.
     Aynı şablonun renk temaları birbirine çok benzer (yüksek korelasyon); farklı kompozisyonlar düşük korelasyon vermelidir.
  3. Ölçüler 1080×1350, taşma yok.
Çıktı: tests/cesitlilik_testi/<marka>.png (karşılaştırma görseli) ve sonuc.json
Çalıştırma: python -m tests.cesitlilik_testi
"""
import json, pathlib, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from tests import mock_gemini as MG
from agent.llm import GeminiClient
from agent.pipeline import ContentPlanner, VisualProducer, approve
from agent import design as DS, series as SR
from agent.render import render_pages
import ornekler_uret as OU

OUT = ROOT / "tests" / "cesitlilik_testi"


def edges(path, size=(54, 68)):
    im = ImageOps.grayscale(Image.open(path).convert("RGB")).resize((270, 338))
    e = im.filter(ImageFilter.FIND_EDGES).resize(size)
    v = list(e.tobytes()); m = sum(v) / len(v)
    return [x - m for x in v]


def corr(a, b):
    num = sum(x * y for x, y in zip(a, b))
    den = (sum(x * x for x in a) * sum(y * y for y in b)) ** .5 or 1
    return num / den


def _font(size=16):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(str(pathlib.Path(__file__).resolve().parent.parent / "templates" / "fonts" / "Montserrat.ttf") if __file__.endswith("cesitlilik_testi.py")
                                  else str(pathlib.Path(__file__).resolve().parent / "templates" / "fonts" / "Montserrat.ttf"), size)
    except Exception:
        return None


def main():
    shutil.rmtree(OUT, ignore_errors=True); OUT.mkdir(parents=True)
    DS.HISTORY = OUT / "_gecmis.json"
    srv = MG.start(8781); MG.STATE["faulty_first_write"] = False
    client = GeminiClient("TEST-KEY", "auto", "http://127.0.0.1:8781", min_interval=0)
    planner, producer = ContentPlanner(client, work_root=OUT / "_is"), VisualProducer(OUT / "_is")
    report, ok = {}, True
    for b, topics in OU.TOPICS.items():
        used, rows = set(), []
        for i, (pf, t) in enumerate(topics, 1):
            if pf != OU.FEED:
                continue
            r0 = planner.start(b, t, platform=pf)
            if r0["status"] == "needs_info":      # ör. son tarih duyurusu: tarih yok → bilgi vermeden devam (tarih uydurulmaz)
                r0 = planner.start(b, t, platform=pf, skip_questions=True)
            plan = r0["plan"]
            first = plan["series"]
            if plan["composition"]["layout"] in used:
                alt = next((a for a in plan["alternatives"] if a["layout"] not in used), None)
                if alt: plan = planner.switch_design(plan, alt["series"])
            used.add(plan["composition"]["layout"])
            res = producer.produce(approve(plan, by="test"), OUT / "_is" / b / f"{i:02d}")
            size = Image.open(res["images"][0]).size
            rows.append(dict(topic=t, first_choice=first, series=plan["series"], name=plan["series_name"], layout=plan["composition"]["layout"],
                             theme=plan.get("theme"), alternatives=[a["series"] for a in plan["alternatives"]],
                             pages=len(res["images"]), size=list(size), overflow=bool(res["overflow"]), image=res["images"][0]))
        sig = [edges(r["image"]) for r in rows]
        pair = [round(corr(sig[x], sig[y]), 3) for x in range(len(sig)) for y in range(x + 1, len(sig))]
        distinct = len({r["layout"] for r in rows}) == len(rows)
        report[b] = dict(posts=rows, distinct_layouts=distinct, max_edge_corr=max(pair), pair_corr=pair)
        ok &= distinct and max(pair) < 0.75 and all(r["size"] == [1080, 1350] and not r["overflow"] for r in rows)
        # karşılaştırma görseli
        W, H, pad = 300, 375, 22
        sh = Image.new("RGB", (pad + 4 * (W + pad), H + 130), "white"); d = ImageDraw.Draw(sh)
        d.text((pad, 10), f"{SR.BRANDS[b]} - SAHTE GEMINI METNIYLE TASARIM SECIMI TESTI (gercek agent ciktisi degildir)", fill="black", font=_font())
        for c, r in enumerate(rows):
            im = Image.open(r["image"]).convert("RGB"); im.thumbnail((W, H)); sh.paste(im, (pad + c * (W + pad), 34))
            d.text((pad + c * (W + pad), 40 + H), f"{r['name']}", fill="black", font=_font())
            d.text((pad + c * (W + pad), 56 + H), f"[{r['layout']}] tema: {r['theme'] or '-'}", fill="black", font=_font())
        sh.save(OUT / f"{b}.png")
    # ölçüt doğrulaması: aynı şablonun renk temaları yüksek korelasyon vermeli
    s = SR.get("aba_psikoloji", "ic_ses"); t, dd = s.build(s.example)[0]
    a, _ = render_pages("aba_psikoloji", [("t1", t, dd)], OUT / "_is" / "olcut", theme="krem")
    c, _ = render_pages("aba_psikoloji", [("t2", t, dd)], OUT / "_is" / "olcut", theme="bordo")
    report["olcut_dogrulama"] = {"ayni_sablon_farkli_renk_corr": round(corr(edges(a[0]), edges(c[0])), 3)}
    srv.shutdown()
    for r in report.values():
        for p in r.get("posts", []): p["image"] = pathlib.Path(p["image"]).name
    (OUT / "sonuc.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree(OUT / "_is", ignore_errors=True)
    for b, r in report.items():
        if b == "olcut_dogrulama":
            print("Ölçüt doğrulama (aynı şablon, iki renk teması):", r); continue
        print(f"{'✓' if r['distinct_layouts'] and r['max_edge_corr'] < .75 else '✗'} {SR.BRANDS[b]}: "
              + " | ".join(f"{p['name']} [{p['layout']}]" for p in r["posts"]) + f" · en yüksek yerleşim benzerliği {r['max_edge_corr']}")
    print("\nÇEŞİTLİLİK TESTİ", "GEÇTİ" if ok else "KALDI")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
