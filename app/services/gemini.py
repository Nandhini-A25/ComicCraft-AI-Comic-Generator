import base64
import io
from typing import Any

from PIL import Image

from app.config import GEMINI_API_KEY, GEMINI_TEXT_MODEL, COMIC_PANELS
from app.models import ComicRequest, OutlineResponse, StoryResponse


class GeminiService:
    def __init__(self) -> None:
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not configured.")
        from google import genai
        self.client = genai.Client(api_key= GEMINI_API_KEY)

    def generate_outline(self, request: ComicRequest) -> OutlineResponse:
        prompt = f"""
You are the story architect for ComicCraft, a 5-panel comic creator.
Create exactly {COMIC_PANELS} connected comic panels.

User story idea: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Requirements:
- Keep the same main character and visual identity across all panels.
- Give the story a clear beginning, escalation, and satisfying ending.
- Each panel needs a concise title, a visual scene description, and a detailed image-generation prompt.
- Image prompts must describe characters, actions, environment, camera framing, lighting, mood, and the requested art style.
- Do not put dialogue text or captions inside the generated images.
- Avoid copyrighted characters, logos, and real-person likenesses.
""".strip()

        interaction = self.client.interactions.create(
            model=GEMINI_TEXT_MODEL,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": OutlineResponse.model_json_schema(),
            },
        )
        result = OutlineResponse.model_validate_json(interaction.output_text)
        if len(result.panels) != COMIC_PANELS:
            raise RuntimeError(f"Gemini returned {len(result.panels)} panels instead of {COMIC_PANELS}.")
        return result

    def generate_story(self, request: ComicRequest, outline: OutlineResponse) -> StoryResponse:
        outline_text = outline.model_dump_json(indent=2)
        prompt = f"""
You are a professional comic scriptwriter.
Expand the supplied {COMIC_PANELS}-panel outline into a polished comic script.

User preferences:
Story idea: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Outline:
{outline_text}

Requirements:
- Return exactly the same number and panel numbers as the outline.
- Preserve continuity between panels.
- Write concise narration suitable for a comic page.
- Add 0-3 natural dialogue lines per panel when appropriate.
- Captions should be short and visual (ambient sound, location, or time cue).
- Keep the image prompt compatible with an image model and consistent with the character.
- Never ask the image model to render written dialogue, captions, speech bubbles, or logos.
""".strip()

        interaction = self.client.interactions.create(
            model=GEMINI_TEXT_MODEL,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": StoryResponse.model_json_schema(),
            },
        )
        result = StoryResponse.model_validate_json(interaction.output_text)
        if len(result.panels) != COMIC_PANELS:
            raise RuntimeError(f"Gemini returned {len(result.panels)} story panels instead of {COMIC_PANELS}.")
        return result

