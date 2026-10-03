from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR, TEMPLATES_DIR, validate_settings
from app.models import ComicRequest
from app.services.comic_service import ComicService
from app.store import store

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _service() -> ComicService:
    validate_settings()
    return ComicService()


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@router.post("/generate")
def generate_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form("Alex"),
    setting: str = Form("enchanted forest"),
    tone: str = Form("adventurous"),
    art_style: str = Form("comic book"),
):
    try:
        payload = ComicRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        comic = _service().generate(payload)
        store.put(comic)
        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={"comic": comic},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": str(exc)},
            status_code=500,
        )


@router.post("/generate-comic/json")
def generate_json(payload: ComicRequest):
    try:
        comic = _service().generate(payload)
        store.put(comic)
        return JSONResponse(comic.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/test-image")
def test_image(prompt: str = Form(...), art_style: str = Form("comic book")):
    try:
        validate_settings()
        from app.services.image_generator import generate_image
        url = generate_image(prompt, art_style)
        return {"success": True, "image_url": url}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/export/{comic_id}")
def export_comic(comic_id: str):
    comic = store.get(comic_id)
    if comic is None:
        raise HTTPException(status_code=404, detail="Comic not found. Generate it again.")

    relative = comic.pdf_url.lstrip("/")
    path = BASE_DIR / relative
    if not path.is_file():
        raise HTTPException(status_code=404, detail="PDF file not found.")

    return FileResponse(path=str(path), media_type="application/pdf", filename=path.name)


@router.get("/export-success")
def export_success(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={},
    )
