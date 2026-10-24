"""Testler için sahte Gemini REST sunucusu (gerçek API ile aynı JSON biçimi).
Gerçek model DEĞİLDİR; yalnızca agent'ın akışını, hata yönetimini ve düzeltme döngüsünü test eder."""
import json, re, sys, threading, copy, pathlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from agent import series as SR

STATE = {"wrap_list": False, "calls": 0, "fail_first_429": False, "daily_quota": False, "faulty_first_write": True, "log": [], "prompts": []}
BRANDS = [("aba_psikoloji", "ABA Psikoloji"), ("aba_egitim", "ABA Eğitim"), ("e4i", "Education for Innovation"), ("design_house", "Design House")]

def brand_of(system):
    return next(b for b, n in BRANDS if f"MARKA: {n}" in system)

def post_type(topic):
    t = topic.lower()
    if any(k in t for k in ("seminer", "etkinlik", "webinar", "açık gün", "workshop", "event")): return "event"
    if any(k in t for k in ("kabul", "admitted", "sonuçlarımız")): return "achievement"
    if any(k in t for k in ("son tarih", "deadline", "son başvuru")): return "deadline"
    return "info"

def vary(x):
    """Gerçek modelin yazacağı gibi örnekten farklı metin üretir (uzun cümlelerde kelime sırası döndürülür)."""
    if isinstance(x, dict): return {k: vary(v) for k, v in x.items()}
    if isinstance(x, list): return [vary(v) for v in x]
    if isinstance(x, str) and len(re.sub(r"<[^>]+>", "", x)) >= 22:
        w = x.split(); return " ".join(w[1:] + w[:1])
    return x

def respond(system, user):
    if "içerik stratejistisin" in system:
        topic = re.search(r"KONU / KULLANICI İSTEĞİ: (.*)", user).group(1)
        lines = [l for l in user.splitlines() if l.startswith("- id='") and "KULLANILAMAZ" not in l]
        ids = [re.search(r"id='(\w+)'", l).group(1) for l in lines]
        tw = {w[:5] for w in re.findall(r"[a-zçğıöşü]{4,}", topic.lower())}
        def sc(l): return len(tw & {w[:5] for w in re.findall(r"[a-zçğıöşü]{4,}", l.lower())})
        ranked = [i for _, i in sorted(((-sc(l), k), ids[k]) for k, l in enumerate(lines))]   # basit "model": kelime örtüşmesi
        pick = "mit" if "mit" in ids and "uyku" in topic.lower() else ranked[0]
        pt = post_type(topic)
        # Model bilerek gereksiz bir soru da önerir; genel postlarda agent bunu sormamalı.
        qs = ["Hedef kitleniz öğrenciler mi, veliler mi?"] if pt == "info" else ["Kayıt bağlantısı var mı?"]
        return {"intent": f"Kullanıcı şu konuda post istiyor: {topic[:60]}", "post_type": pt, "questions": qs,
                "series": pick, "reason": "Konu bu serinin amacına uygun.", "angle": "Konunun ana fikri", "audience": "öğrenci",
                "alternatives": [i for i in ranked if i != pick][:2], "design_reason": "Konunun yoğunluğuna uygun kompozisyon."}
    if "denetçisisin" in system:
        return {"score": 9, "issues": [], "summary": "Marka diline uygun."}
    brand = brand_of(system)
    m = re.search(r"(?:SEÇİLEN SERİ|SERİ): (.+?)(?: \(|\n)", user)
    nm = m.group(1).strip()
    pool = [x for lst in SR.PLATFORM_SERIES.values() for x in lst[brand]]
    ser = next(x for x in pool if x.name == nm or x.name.startswith(nm + " ("))
    fields = vary(copy.deepcopy(ser.example))
    lang_en = "English" in system
    cap = ("Sample caption written for the topic.\n\nSecond paragraph.\n\nSave this post." if lang_en else "Konuya uygun örnek caption.\n\nİkinci paragraf.\n\nBirlikte planlayalım.")
    tags = ["#Test", "#Ornek", "#Konu", "#Marka", "#Instagram"]
    if "geri bildirimine göre" in system:
        cur = json.loads(re.search(r"KULLANICIYA SUNULAN TASLAK:\n(.*?)\n\nKULLANICININ", user, re.S).group(1))
        fb = re.search(r"KULLANICININ GERİ BİLDİRİMİ:\n(.*?)\n\n", user, re.S).group(1)
        out = dict(cur, caption=cur["caption"] + (" Updated after feedback." if lang_en else " Geri bildirime göre güncellendi."))
        out["not"] = "Logo ve renkler marka kuralı gereği değiştirilmedi." if "logo" in fb.lower() or "renk" in fb.lower() else ""
        fl = fb.lower()
        if any(k in fl for k in ("infografik", "carousel", "başka tasarım", "minimal", "fotoğraf", "infographic")):
            opts = re.findall(r"- id='(\w+)'[^\n]*", user.split("KULLANILABİLİR DİĞER TASARIMLAR")[1])
            lines = re.findall(r"- id='\w+'[^\n]*", user.split("KULLANILABİLİR DİĞER TASARIMLAR")[1])
            key = "infografik" if "infografik" in fl else "carousel" if "carousel" in fl else ""
            hit = [re.search(r"id='(\w+)'", l).group(1) for l in lines if key and key in l.lower()]
            out["switch_series"] = (hit or opts)[0]
        return out
    if "metin yazarısın. Post kütüphanesindeki" in system and STATE["faulty_first_write"]:
        # Kasıtlı hatalar: uzun alan + doğrulanmamış istatistik → agent düzeltme turuna girmeli
        k = next(k for k, v in ser.schema.items() if isinstance(v, SR.S))
        fields[k] = (str(fields[k]) + " ") * 6
        cap = cap + (" Students improve by 87% in 3 weeks." if lang_en else " Öğrencilerin %87'si 3 haftada başarıya ulaşıyor.")
    return {"fields": fields, "caption": cap, "hashtags": tags if ser.kind != "story" else tags[:2],
            "self_check": [{"rule": "Kontrol listesi", "ok": True, "note": ""}]}

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.headers.get("x-goog-api-key") != "TEST-KEY": return self._send(400, {"error": {"message": "API key not valid."}})
        self._send(200, {"models": [{"name": f"models/{n}", "supportedGenerationMethods": ["generateContent"]} for n in
                                    ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-3.5-flash-lite", "text-embedding-004"]]})
    def do_POST(self):
        n = int(self.headers["Content-Length"]); body = json.loads(self.rfile.read(n))
        STATE["calls"] += 1
        if STATE["daily_quota"]:
            return self._send(429, {"error": {"code": 429, "message": "Quota exceeded", "details": [{"violations": [{"quotaId": "GenerateRequestsPerDayPerProjectPerModel-FreeTier"}]}]}})
        if STATE["fail_first_429"] and STATE["calls"] == 1:
            return self._send(429, {"error": {"code": 429, "message": "rate", "details": [{"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "1s"}]}})
        system = body["systemInstruction"]["parts"][0]["text"]; user = body["contents"][0]["parts"][0]["text"]
        STATE["prompts"].append((system[:80], user[:300]))
        out = respond(system, user)
        if STATE["wrap_list"]:   # gerçek Gemini'nin bazen yaptığı gibi nesneyi listeye sarar
            out = [out]
        if "metin yazarısın. Post kütüphanesindeki" in system: STATE["faulty_first_write"] = False
        STATE["log"].append(self.path.split("/models/")[1].split(":")[0])
        self._send(200, {"candidates": [{"content": {"parts": [{"text": json.dumps(out, ensure_ascii=False)}]}}], "usageMetadata": {"totalTokenCount": 1000}})

def start(port=8765):
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv
