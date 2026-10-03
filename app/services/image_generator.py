from pathlib import Path
from uuid import uuid4

from huggingface_hub import InferenceClient

from app.config import (
    HF_TOKEN,
    HF_IMAGE_MODEL,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    PANELS_DIR,
)

client = InferenceClient(
    api_key=HF_TOKEN,
    timeout=300,
)


def generate_image(prompt: str, art_style: str) -> str:
    final_prompt = f"""
Create one high-quality comic illustration.

Art style: {art_style}
Scene: {prompt}

Visual requirements:
- cinematic comic composition
- consistent character appearance
- expressive face and pose
- detailed foreground and background
- professional digital illustration
- dramatic but natural lighting
- clear subject separation
- no text
- no speech bubbles
- no captions
- no logos
- no watermark
""".strip()

    negative_prompt = (
        "text, letters, words, captions, speech bubbles, logo, watermark, "
        "signature, blurry, low quality, distorted anatomy, duplicate characters"
    )

    try:
        image = client.text_to_image(
            prompt=final_prompt,
            negative_prompt=negative_prompt,
            width=IMAGE_WIDTH,
            height=IMAGE_HEIGHT,
            model=HF_IMAGE_MODEL,
        )

    except Exception as exc:
        raise RuntimeError(
            f"Hugging Face image generation failed. "
            f"Model={HF_IMAGE_MODEL}. Details: {exc}"
        ) from exc

    filename = f"panel_{uuid4().hex}.png"
    path: Path = PANELS_DIR / filename

    image.save(path, format="PNG", optimize=True)

    return f"/static/panels/{filename}"