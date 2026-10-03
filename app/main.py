from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR
from app.routes import router

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="Generate five-panel AI comics with Gemini text and image models.",
    version="2.0.0",
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.include_router(router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}
