"""Markaların görünüm temaları (zemin seçenekleri). Tanımlar templates/brands/<marka>.py içindeki THEMES sözlüğündedir.
Temalar yalnızca Brand Kit paletindeki renkleri kullanır; logo, font ve iletişim bandı her temada aynıdır."""
import hashlib, importlib, pathlib, sys

_T = pathlib.Path(__file__).resolve().parent.parent / "templates"


def _mod(brand):
    for p in (str(_T), str(_T / "brands")):
        if p not in sys.path: sys.path.insert(0, p)
    return importlib.import_module(brand)


def options(brand):
    """{tema_id: görünen ad}"""
    return {k: v["name"] for k, v in getattr(_mod(brand), "THEMES", {}).items()}


def themable(brand, series):
    """Uzman / blog serisi gibi kendi sabit düzeni olan serilerde tema yok."""
    no = getattr(_mod(brand), "NO_THEME", set())
    return not any(t in no for t, _ in series.build(series.example))


def pick(brand, series, topic, suggested=None):
    """Modelin önerdiği tema geçerliyse o; değilse konuya göre sabit ama konudan konuya değişen bir tema."""
    if not themable(brand, series):
        return None
    opts = list(options(brand))
    if suggested in opts:
        return suggested
    if not opts:
        return None
    h = int(hashlib.md5(f"{series.id}|{topic}".encode("utf-8")).hexdigest(), 16)
    return opts[h % len(opts)]
