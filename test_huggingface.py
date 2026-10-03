from huggingface_hub import InferenceClient
from app.config import HF_TOKEN, HF_IMAGE_MODEL, HF_PROVIDER, IMAGE_WIDTH, IMAGE_HEIGHT

print("HF token loaded:", bool(HF_TOKEN))
print("HF model:", HF_IMAGE_MODEL)

client = InferenceClient(
    provider=HF_PROVIDER,
    api_key=HF_TOKEN,
    timeout=300,
)

prompt = """
A high-quality cinematic comic illustration of a young engineer
standing at a construction site during sunset, expressive face,
dramatic lighting, detailed buildings and construction equipment,
professional digital comic art, no text, no speech bubbles,
no watermark.
"""

print("Generating image...")

image = client.text_to_image(
    prompt,
    width=IMAGE_WIDTH,
    height=IMAGE_HEIGHT,
    model=HF_IMAGE_MODEL,
)

output = "test_huggingface_image.png"
image.save(output)

print(f"SUCCESS! Image saved as {output}")