"""Şablon sayfalarını PNG'ye çevirir (ayrı süreçte)."""
import json, os, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

def render_pages(brand, pages, out_dir, photo=None, photo_opacity=0.3, timeout=180, measure_only=False, theme=None):
    """measure_only=True: PNG yazmaz, yalnızca taşmayı ölçer (Agent 1). False: PNG üretir (Agent 2)."""
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    req = {"brand": brand, "out": str(out), "pages": [{"name": n, "template": t, "data": d} for n, t, d in pages],
           "photo": photo, "photo_opacity": photo_opacity, "shots": not measure_only, "theme": theme}
    rp = out / "_render_request.json"
    rp.write_text(json.dumps(req, ensure_ascii=False), encoding="utf-8")
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-m", "agent.render_worker", str(rp)], cwd=str(ROOT), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=timeout, env=env)
    if r.returncode != 0:
        raise RuntimeError("Görsel üretilemedi:\n" + (r.stderr or r.stdout)[-2000:])
    rep = json.loads((out / "_render_report.json").read_text(encoding="utf-8"))
    rp.unlink(missing_ok=True); (out / "_render_report.json").unlink(missing_ok=True)
    return ([] if measure_only else [str(out / f"{n}.png") for n, _, _ in pages]), rep["overflow"]
