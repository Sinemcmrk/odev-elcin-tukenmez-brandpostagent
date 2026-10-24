"""Kullanıcı onayı.

Onay, planın içeriğinin parmak izine (SHA-256) bağlanır. Onaydan sonra plan içeriği değişirse
(metin, seri, platform, fotoğraf) parmak izi tutmaz ve Agent 2 görsel üretmeyi reddeder.
Böylece onay yalnızca bir arayüz butonu değil, üretim aşamasının kod düzeyindeki ön koşuludur.
"""
import datetime, hashlib, json

HASHED = ("brand", "platform", "series", "theme", "content", "photo", "photo_opacity")


class ApprovalError(Exception):
    """Onaylanmamış ya da onaydan sonra değiştirilmiş plan."""


def content_hash(plan):
    core = {k: plan.get(k) for k in HASHED}
    return hashlib.sha256(json.dumps(core, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def approve(plan, by="kullanıcı", note=""):
    """Planın onaylı bir kopyasını döndürür.
    Biçimsel uyarısı kalmış planlar onaylanabilir; kullanıcının vermediği sayı/tarih içeren plan onaylanamaz."""
    if plan.get("status") != "ready":
        raise ApprovalError("Yalnızca hazır (soruları tamamlanmış) bir plan onaylanabilir.")
    from .validate import blocking
    bad = blocking(plan.get("checks", {}).get("remaining_warnings"))
    if bad:
        raise ApprovalError("Bu plan onaylanamaz: içinde sizin vermediğiniz bir sayı, istatistik ya da tarih var. "
                            "Geri bildirimle düzeltin ya da doğru bilgiyi 'Doğrulanmış bilgi' alanına yazıp yeniden planlayın. → " + " | ".join(bad))
    p = json.loads(json.dumps(plan, ensure_ascii=False))
    p["approval"] = {"status": "approved", "by": by, "note": note,
                     "at": datetime.datetime.now().isoformat(timespec="seconds"), "hash": content_hash(p)}
    return p


def check(plan):
    """Onay geçerli değilse ApprovalError fırlatır."""
    a = plan.get("approval") or {}
    if a.get("status") != "approved":
        raise ApprovalError("Plan henüz onaylanmadı. Agent 2 yalnızca kullanıcının onayladığı planla görsel üretir.")
    if a.get("hash") != content_hash(plan):
        raise ApprovalError("Plan onaydan sonra değiştirilmiş. Değişen planın yeniden onaylanması gerekir.")


def is_approved(plan):
    try:
        check(plan); return True
    except ApprovalError:
        return False
