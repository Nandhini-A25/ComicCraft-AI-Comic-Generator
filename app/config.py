from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_TEXT_MODEL = os.getenv("GEMINI_TEXT_MODEL", "gemini-3.8-flash").strip()
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_IMAGE_MODEL = os.getenv("HF_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell").strip()
HF_PROVIDER = os.getenv("HF_PROVIDER", "auto").strip()
COMIC_PANELS = int(os.getenv("COMIC_PANELS", "5"))
IMAGE_WIDTH = int(os.getenv("IMAGE_WIDTH", "768"))
IMAGE_HEIGHT = int(os.getenv("IMAGE_HEIGHT", "768"))
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"
PANELS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


def validate_settings() -> None:
    if not GEMINI_API_KEY or GEMINI_API_KEY.startswith("your_"):
        raise RuntimeError("GEMINI_API_KEY is missing. Put your real Gemini key in .env")
    if not HF_TOKEN or HF_TOKEN.startswith("hf_your_"):
        raise RuntimeError("HF_TOKEN is missing. Put your real Hugging Face token in .env")
