"""Platform tanımları.

Şirketin verdiği referanslar Instagram hesapları ve web siteleridir; bu yüzden ana platform Instagram Feed'dir.
Instagram Story ikincil seçenektir (her marka için bir Story düzeni).

Yeni bir platform (ör. LinkedIn 1200×1500) eklemek için:
  1) Aşağıya bir Platform kaydı ekleyin (enabled=True),
  2) templates/brands/<marka>.py içine o ölçüde bir şablon fonksiyonu yazın,
  3) agent/series.py içinde PLATFORM_SERIES[<platform_id>] altında o şablonu kullanan seriyi tanımlayın.
Agent 1 ve Agent 2 platformu yalnızca bu kayıttan okur; başka bir yeri değiştirmek gerekmez.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Platform:
    id: str
    name: str
    width: int
    height: int
    ratio: str
    note: str
    enabled: bool = True


PLATFORMS = {
    "instagram_feed": Platform("instagram_feed", "Instagram Feed", 1080, 1350, "4:5",
                               "Ana platform. Post Kütüphanesindeki tüm seriler; tek post veya kaydırmalı (carousel)."),
    "instagram_story": Platform("instagram_story", "Instagram Story", 1080, 1920, "9:16",
                                "İkincil platform. Her marka için tek sayfalık Story düzeni; üst ~250 px ve alt ~280 px "
                                "Instagram arayüzüyle örtüşebileceği için ana metin bu bantların dışında tutulur."),
    "linkedin": Platform("linkedin", "LinkedIn (planlandı)", 1200, 1500, "4:5",
                         "Henüz etkin değil. Şirketin paylaştığı referanslarda LinkedIn hesabı yok.", enabled=False),
}

DEFAULT = "instagram_feed"


def enabled():
    return {k: p for k, p in PLATFORMS.items() if p.enabled}


def get(pid):
    p = PLATFORMS.get(pid)
    if not p or not p.enabled:
        raise ValueError(f"Desteklenmeyen platform: {pid}. Seçenekler: {', '.join(enabled())}")
    return p
