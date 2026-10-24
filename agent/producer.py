"""AGENT 2 — Visual Production Agent.

Yalnızca kullanıcının onayladığı plan JSON'u ile çalışır (agent/approval.py). LLM kullanmaz:
Post Kütüphanesinin HTML/CSS şablonlarını Playwright ile PNG'ye çevirir. Carousel'de tüm sayfaları üretir.

Marka kimliği kilidi: plan yalnızca METİN taşır. Renk, font, logo ve yerleşim şablon kodunda sabittir;
plan alanları üretimden önce şemaya göre yeniden temizlenir (izin verilmeyen HTML/stil kaçırılır).

Komut satırı:  python -m agent.producer onayli_plan.json [cikis_klasoru]
"""
import datetime, json, pathlib, sys, time
from . import series as SR, validate as V, platforms as PF, approval as AP, design as DS
from .render import render_pages

ROOT = pathlib.Path(__file__).resolve().parent.parent


def slug(s, n=40):
    import re
    tr = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return re.sub(r"[^a-z0-9]+", "-", s.translate(tr).lower()).strip("-")[:n] or "post"


class VisualProducer:
    def __init__(self, out_root=None):
        self.out_root = pathlib.Path(out_root or ROOT / "outputs")

    def produce(self, plan, out_dir=None, on_step=None):
        say = on_step or (lambda step, msg, data=None: None)
        AP.check(plan)                                  # onay yoksa / değiştiyse burada durur
        t0 = time.time()
        brand, platform = plan["brand"], plan["platform"]
        if brand not in SR.BRANDS:
            raise ValueError(f"Bilinmeyen marka: {brand}")
        pf = PF.get(platform)
        ser = SR.get(brand, plan["series"], platform)
        fields, _ = V.check_schema(ser.schema, plan["content"]["fields"])   # kimlik kilidi: yalnızca izinli metin
        built = ser.build(fields)
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        out = pathlib.Path(out_dir) if out_dir else self.out_root / f"{stamp}-{brand}-{platform}-{ser.id}-{slug(plan['topic'], 30)}"
        pages = [(f"{brand}-{ser.id}-{k + 1:02d}", t, d) for k, (t, d) in enumerate(built)]
        say("render", f"{len(pages)} sayfa çiziliyor ({pf.name}, {pf.width}×{pf.height})…")
        pngs, overflow = render_pages(brand, pages, out, plan.get("photo"), plan.get("photo_opacity", 0.3), theme=plan.get("theme"))
        say("render", f"{len(pngs)} PNG oluşturuldu.", {"files": [pathlib.Path(p).name for p in pngs]})

        c = plan["content"]
        (out / "caption.txt").write_text(c["caption"] + "\n\n" + " ".join(c["hashtags"]), encoding="utf-8")
        (out / "plan_onayli.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        result = {
            "brand": brand, "brand_name": SR.BRANDS[brand], "platform": platform, "platform_name": pf.name,
            "size": [pf.width, pf.height], "series": ser.id, "series_name": ser.name, "kind": ser.kind, "theme": plan.get("theme"),
            "topic": plan["topic"], "plan_id": plan["plan_id"], "plan_version": plan["version"],
            "approved_at": plan["approval"]["at"], "approved_by": plan["approval"]["by"],
            "caption": c["caption"], "hashtags": c["hashtags"], "fields": fields,
            "overflow": {k: v for k, v in overflow.items() if v}, "out_dir": str(out), "images": [str(p) for p in pngs],
            "seconds": round(time.time() - t0, 1),
        }
        (out / "post.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        DS.record(brand, ser.id, plan["topic"])        # çeşitlilik geçmişi: sonraki planda farklı kompozisyon tercih edilir
        say("done", f"Tamamlandı: {len(pngs)} PNG · {result['seconds']} sn")
        return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Kullanım: python -m agent.producer onayli_plan.json [cikis_klasoru]")
    p = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    try:
        r = VisualProducer().produce(p, sys.argv[2] if len(sys.argv) > 2 else None, on_step=lambda s, m, d=None: print(m))
        print("\n".join(r["images"]))
    except AP.ApprovalError as e:
        sys.exit(f"Üretim reddedildi: {e}")
