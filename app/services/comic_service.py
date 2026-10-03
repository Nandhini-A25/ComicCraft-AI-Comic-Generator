from uuid import uuid4

from app.config import COMIC_PANELS
from app.models import ComicRequest, ComicResult
from app.services.gemini import GeminiService
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.pdf_exporter import save_pdf


class ComicService:
    def __init__(self) -> None:
        self.gemini = GeminiService()

    def generate(self, request: ComicRequest) -> ComicResult:
        outline = self.gemini.generate_outline(request)
        story = self.gemini.generate_story(request, outline)

        if len(story.panels) != COMIC_PANELS:
            raise RuntimeError(
                f"Expected {COMIC_PANELS} story panels, got {len(story.panels)}."
            )

        image_urls = []
        for panel in story.panels:
            image_urls.append(generate_image(panel.image_prompt, request.art_style))

        layout = build_comic_layout(story, image_urls)
        comic_id = uuid4().hex
        title = f"{request.character_name}'s Comic Adventure"
        pdf_url = save_pdf(title, layout)

        return ComicResult(
            comic_id=comic_id,
            title=title,
            panels=layout,
            pdf_url=pdf_url,
        )
