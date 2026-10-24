"""Arayüz akış testi (Streamlit kurulmadan).

Streamlit'in yerine geçen küçük bir taklit modülle app.py baştan sona çalıştırılır; butonlara "basılır",
alanlara değer yazılır, st.rerun() gerçek uygulamadaki gibi betiği yeniden başlatır. Gemini yerine sahte sunucu kullanılır.
Gerçek tarayıcı görünümünü test ETMEZ; yalnızca akışı, durum geçişlerini ve onay kapısını doğrular.
Çalıştırma: python -m tests.app_smoke
"""
import os, sys, types, pathlib, runpy, traceback
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tests import mock_gemini as MG

class Rerun(Exception): pass

class SS(dict):
    __getattr__ = dict.get
    def __setattr__(self, k, v): self[k] = v

class W:
    """Her Streamlit çağrısını karşılayan nesne (konteyner, status, sütun...)."""
    def __init__(self, ui): self.ui = ui
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def __getattr__(self, name): return getattr(self.ui, name)

class UI(types.ModuleType):
    def __init__(self):
        super().__init__("streamlit")
        self.session_state, self.values, self.clicks, self.seen, self.errors = SS(), {}, set(), [], []
    # yerleşim
    def set_page_config(self, **k): pass
    def tabs(self, labels): return [W(self) for _ in labels]
    def columns(self, spec, **k): return [W(self) for _ in range(spec if isinstance(spec, int) else len(spec))]
    def expander(self, *a, **k): return W(self)
    def status(self, *a, **k): return W(self)
    @property
    def sidebar(self): return W(self)
    # çıktı
    def _out(self, *a, **k): self.seen.append(" ".join(str(x) for x in a))
    markdown = title = header = subheader = caption = info = success = code = json = table = image = write = toast = divider = _out
    def warning(self, *a, **k): self._out(*a); self.seen.append("UYARI")
    def error(self, *a, **k): self._out(*a); self.errors.append(str(a[0]))
    def update(self, **k): self.seen.append(k.get("label", ""))
    # girdiler
    def button(self, label, **k):
        if k.get("on_click") and label in self.clicks: self.clicks.discard(label); k["on_click"](*k.get("args", ())); return False
        hit = label in self.clicks and not k.get("disabled"); self.clicks.discard(label) if hit else None; return hit
    def download_button(self, label, data, **k): self.seen.append(f"İNDİR:{label}:{len(data)}"); return False
    def toggle(self, label, value=False, **k): return self.values.get(label, value)
    def _choice(self, label, options, format_func=str, **k):
        opts = list(options); [format_func(o) for o in opts]
        v = self.values.get(label, opts[0]); return v if v in opts else opts[0]
    selectbox = radio = _choice
    def text_area(self, label, value="", **k): return self.values.get(label, value)
    text_input = text_area
    def slider(self, label, a, b, v, *x, **k): return v
    def file_uploader(self, *a, **k): return None
    def rerun(self): raise Rerun()

def run_app(ui, clicks=(), values=None, max_reruns=4):
    ui.clicks, ui.seen = set(clicks), []
    ui.values.update(values or {})
    for _ in range(max_reruns):
        try:
            runpy.run_path(str(ROOT / "app.py"), run_name="__main__"); return
        except Rerun:
            ui.clicks = set()

def main():
    srv = MG.start(8768)
    os.environ.update(GEMINI_API_KEY="TEST-KEY", GEMINI_BASE_URL="http://127.0.0.1:8768", GEMINI_MIN_INTERVAL="0", AGENT_DEEP_REVIEW="1")
    ui = UI(); sys.modules["streamlit"] = ui
    S = ui.session_state
    ok = []
    def check(name, cond):
        ok.append(cond); print(("✓ " if cond else "✗ ") + name)

    # Senaryo 1: genel post (Feed) → plan → onay → PNG
    MG.STATE["faulty_first_write"] = True
    run_app(ui)
    check("İlk ekran: istek aşaması, görsel yok", S.stage == "input" and S.result is None)
    run_app(ui, ["ABA Psikoloji", "1 · Plan hazırla (Agent 1)"], {"Post konusu / isteğiniz": "Sınav öncesi uyku hakkında yanlış bilinenler"})
    check("Agent 1 planı hazırladı, onay bekleniyor (PNG yok)", S.stage == "review" and S.plan and S.plan["approval"]["status"] == "pending" and S.result is None)
    check("Plan ekranında tasarım planı ve karar butonları var", any("Tasarım planı" in x for x in ui.seen))
    run_app(ui, ["💬 Geri bildirimi uygula (Agent 1)"], {f"Geri bildirim / değişiklik isteği": "CTA daha samimi olsun"})
    check("Geri bildirim: plan v2, hâlâ onay bekliyor", S.plan["version"] == 2 and S.stage == "review" and S.result is None)
    th0 = S.plan.get("theme")
    other = next(t for t in ("krem", "koyu", "bordo") if t != th0)
    run_app(ui, ["Görünümü uygula"], {"Görünümü değiştir (Brand Kit renkleri içinde)": other})
    check("Görünüm değişikliği: yeni plan sürümü, tema değişti", S.plan["version"] == 3 and S.plan["theme"] == other)
    run_app(ui, ["Düzenlemeyi kaydet (yeni plan sürümü)"], {"Caption": "Elle düzenlenmiş caption.\n\nBirlikte planlayalım."})
    check("Elle düzenleme: plan v4, caption değişti", S.plan["version"] == 4 and S.plan["content"]["caption"].startswith("Elle düzenlenmiş"))
    v0, s0 = S.plan["version"], S.plan["series"]
    run_app(ui, ["Bu tasarımı dene"])
    check("Başka tasarım dene: farklı seri, yeni sürüm", S.plan["series"] != s0 and S.plan["version"] == v0 + 1 and S.stage == "review")
    run_app(ui, ["✅ Onayla ve görseli üret (Agent 2)"])
    check("Onay sonrası Agent 2: PNG üretildi", S.stage == "done" and len(S.result["images"]) >= 1 and all(pathlib.Path(p).exists() for p in S.result["images"]))
    check("İndirme butonları gösterildi", sum(x.startswith("İNDİR:PNG") for x in ui.seen) == len(S.result["images"]) and any("ZIP" in x for x in ui.seen))
    run_app(ui, ["↺ Yeni post (baştan başla)"])
    check("Yeni post: akış sıfırlandı", S.stage == "input" and S.plan is None)

    # Senaryo 2: etkinlik duyurusu (Story) → soru → yanıt → plan → onay → 1080×1920 PNG
    run_app(ui, ["ABA Eğitim", "1 · Plan hazırla (Agent 1)"], {"Platform": "instagram_story",
                                                "Post konusu / isteğiniz": "Bebek ofisimizde ücretsiz IELTS semineri düzenliyoruz"})
    check("Eksik bilgi: Agent 1 soru sordu", S.stage == "questions" and any("tarih" in q.lower() for q in S.questions))
    q0 = S.questions[0]
    run_app(ui, ["Yanıtlarla devam et"], {q0: "12 Kasım 2026 Pazar 14.00, Bebek ofisi"})
    check("Yanıt sonrası plan hazır (Story, 1080×1920)", S.stage == "review" and S.plan["design"]["size"] == "1080×1920")
    run_app(ui, ["✅ Onayla ve görseli üret (Agent 2)"])
    from PIL import Image
    check("Story PNG üretildi (1080×1920)", S.stage == "done" and Image.open(S.result["images"][0]).size == (1080, 1920))
    check("Marka kartlarıyla seçim: ABA Eğitim planı", S.plan["brand"] == "aba_egitim")
    check("Arayüzde hata mesajı yok", not ui.errors)
    if ui.errors: print(ui.errors)
    srv.shutdown()
    print(f"\n{sum(ok)}/{len(ok)} arayüz kontrolü geçti")
    sys.exit(0 if all(ok) else 1)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc(); sys.exit(1)
