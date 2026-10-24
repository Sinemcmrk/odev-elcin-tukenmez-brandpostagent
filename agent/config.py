"""Ayarlar .env dosyasından okunur (python-dotenv yoksa basit okuyucu kullanılır)."""
import os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_env():
    path = ROOT / ".env"
    try:
        from dotenv import load_dotenv
        load_dotenv(path)
    except ImportError:
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return {
        "api_key": os.environ.get("GEMINI_API_KEY", "").strip(),
        "model": os.environ.get("GEMINI_MODEL", "auto").strip() or "auto",
        "base_url": os.environ.get("GEMINI_BASE_URL", "").strip() or None,
        "min_interval": float(os.environ.get("GEMINI_MIN_INTERVAL", "4")),
        "deep_review": os.environ.get("AGENT_DEEP_REVIEW", "1") != "0",
    }


def make_client(log=None):
    from .llm import GeminiClient
    c = load_env()
    return GeminiClient(c["api_key"], c["model"], c["base_url"], c["min_interval"], log=log), c
