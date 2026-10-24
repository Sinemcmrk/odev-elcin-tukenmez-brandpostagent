"""Google Gemini istemcisi (resmi REST API, ek SDK gerektirmez).

- Yalnızca ücretsiz katmanda sunulan Flash / Flash-Lite ailesinden model seçer.
- Kota (429) hatasında bekler, tekrar dener; günlük kota bittiyse açık bir hata verir.
- Hiçbir durumda başka (ücretli) bir servise geçmez.
"""
import json, os, re, time
import requests

DEFAULT_BASE = "https://generativelanguage.googleapis.com"
# Tercih sırası: önce günlük kotası yüksek Flash-Lite modelleri, sonra Flash.
PREFERRED = [
    "gemini-flash-lite-latest", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-2.5-flash-lite",
    "gemini-flash-latest", "gemini-3.8-flash", "gemini-3.6-flash", "gemini-2.5-flash",
]
EXCLUDE = ("pro", "image", "tts", "live", "embedding", "audio", "robotics", "vision", "aqa", "learnlm", "gemma", "omni", "veo", "lyria", "nano")


class LLMError(Exception):
    pass


class QuotaExceeded(LLMError):
    pass


class GeminiClient:
    def __init__(self, api_key, model="auto", base_url=None, min_interval=4.0, max_retries=3, log=None):
        if not api_key:
            raise LLMError("GEMINI_API_KEY bulunamadı. .env dosyasına anahtarınızı yazın.")
        self.key = api_key
        self.base = (base_url or DEFAULT_BASE).rstrip("/")
        self.min_interval = float(min_interval)
        self.max_retries = int(max_retries)
        self._last = 0.0
        self.calls = 0
        self.tokens = 0
        self.log = log or (lambda m: None)
        self.auto = (not model or model == "auto")
        self.candidates = self.rank_models() if self.auto else [model]
        self.model = self.candidates[0]

    # ---------------------------------------------------------------- modeller
    def list_models(self):
        r = requests.get(f"{self.base}/v1beta/models", params={"pageSize": 200},
                         headers={"x-goog-api-key": self.key}, timeout=30)
        if r.status_code != 200:
            raise LLMError(self._explain(r))
        out = []
        for m in r.json().get("models", []):
            if "generateContent" in m.get("supportedGenerationMethods", []):
                out.append(m["name"].split("/", 1)[-1])
        return out

    def rank_models(self):
        """Ücretsiz Flash/Flash-Lite ailesinden, erişilebilir modelleri tercih sırasına dizer."""
        names = self.list_models()
        ranked = [p for p in PREFERRED if p in names]
        for fam in ("flash-lite", "flash"):
            ranked += sorted([n for n in names if fam in n and n not in ranked and not any(x in n for x in EXCLUDE)], reverse=True)
        if not ranked:
            raise LLMError("Bu API anahtarıyla kullanılabilir bir Gemini Flash modeli bulunamadı. Bulunan modeller: " + ", ".join(names[:15]))
        return ranked

    def _next_model(self, why):
        """Otomatik modda bir sonraki ücretsiz modele geçer (ücretli servise asla geçmez)."""
        if self.auto and len(self.candidates) > 1:
            old = self.candidates.pop(0); self.model = self.candidates[0]
            self.log(f"{old} kullanılamadı ({why}); {self.model} modeline geçiliyor.")
            return True
        return False

    # ---------------------------------------------------------------- çağrı
    def _explain(self, r):
        try:
            err = r.json().get("error", {})
            msg = err.get("message", "")
        except Exception:
            msg = r.text[:300]
        if r.status_code == 400 and "API key" in msg:
            return "API anahtarı geçersiz. .env dosyasındaki GEMINI_API_KEY değerini kontrol edin."
        if r.status_code == 403:
            return "Bu anahtarın bu modele erişim izni yok (403). Google AI Studio'dan yeni bir anahtar oluşturun. Ayrıntı: " + msg
        if r.status_code == 404:
            return f"Model bulunamadı (404): {self.__dict__.get('model')}. .env içinde GEMINI_MODEL=auto yapın. Ayrıntı: {msg}"
        if r.status_code == 402:
            return "Faturalandırma hatası (402). Bu proje ücretsiz katmanda kalmalı; Google Cloud'da faturalandırmayı açmayın."
        return f"Gemini hatası {r.status_code}: {msg}"

    def _wait_interval(self):
        dt = time.time() - self._last
        if dt < self.min_interval:
            time.sleep(self.min_interval - dt)
        self._last = time.time()

    def generate_json(self, system, user, temperature=0.8):
        body = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": temperature, "maxOutputTokens": 8192},
        }
        parse_retry = False
        for attempt in range(self.max_retries + 2):
            url = f"{self.base}/v1beta/models/{self.model}:generateContent"
            self._wait_interval()
            try:
                r = requests.post(url, json=body, headers={"x-goog-api-key": self.key}, timeout=120)
            except requests.RequestException as e:
                if attempt < self.max_retries:
                    time.sleep(5 * (attempt + 1)); continue
                raise LLMError(f"Gemini'ye bağlanılamadı: {e}")
            self.calls += 1
            if r.status_code == 429:
                info = r.text
                if "PerDay" in info or "per day" in info.lower():
                    if self._next_model("günlük kota doldu"): continue
                    raise QuotaExceeded("Ücretsiz katmanın günlük kotası doldu. Kota Pasifik saatiyle gece yarısı (Türkiye saatiyle 10.00 civarı) yenilenir. "
                                        "İsterseniz .env içinde GEMINI_MODEL ile günlük kotası daha yüksek bir Flash-Lite modeli seçin.")
                m = re.search(r'"retryDelay":\s*"(\d+)', info)
                delay = min(int(m.group(1)) + 1 if m else 15 * (attempt + 1), 65)
                if attempt < self.max_retries:
                    self.log(f"Dakikalık kota sınırı: {delay} sn bekleniyor…")
                    time.sleep(delay); continue
                raise QuotaExceeded("Ücretsiz katmanın dakikalık sınırına takıldı. Bir dakika sonra tekrar deneyin.")
            if r.status_code in (500, 502, 503, 504):
                if attempt < self.max_retries:
                    self.log("Gemini geçici olarak yoğun, tekrar deneniyor…")
                    time.sleep(8 * (attempt + 1)); continue
            if r.status_code in (403, 404) and self._next_model(f"HTTP {r.status_code}"):
                continue
            if r.status_code != 200:
                raise LLMError(self._explain(r))
            data = r.json()
            self.tokens += data.get("usageMetadata", {}).get("totalTokenCount", 0)
            try:
                parts = data["candidates"][0]["content"]["parts"]
                text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
            except (KeyError, IndexError):
                reason = data.get("promptFeedback", {}).get("blockReason") or data.get("candidates", [{}])[0].get("finishReason")
                raise LLMError(f"Model boş yanıt verdi ({reason}). Konuyu farklı ifade edip tekrar deneyin.")
            try:
                return parse_json(text)
            except ValueError:
                if not parse_retry:
                    parse_retry = True
                    body["contents"][0]["parts"][0]["text"] = user + "\n\nYanıtın YALNIZCA geçerli bir JSON nesnesi olmalı."
                    continue
                raise LLMError("Model geçerli JSON döndürmedi.")
        raise LLMError("Gemini isteği tamamlanamadı.")


def _as_object(v):
    """Agent her zaman bir JSON nesnesi bekler. Model nesneyi bir listeye sararsa ([{...}]) içindeki nesne alınır."""
    if isinstance(v, dict):
        return v
    if isinstance(v, list):
        objs = [x for x in v if isinstance(x, dict)]
        if objs:
            return objs[0]
    raise ValueError("JSON nesnesi değil")


def parse_json(text):
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    try:
        return _as_object(json.loads(t))
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", t, re.S)
        if m:
            try:
                return _as_object(json.loads(m.group(0)))
            except json.JSONDecodeError:
                pass
    raise ValueError("JSON değil")
