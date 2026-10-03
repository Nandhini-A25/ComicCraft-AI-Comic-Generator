from huggingface_hub import InferenceClient
from app.config import HF_TOKEN, HF_IMAGE_MODEL, HF_PROVIDER, IMAGE_WIDTH, IMAGE_HEIGHT
import os, time

print("HF token loaded:", bool(HF_TOKEN))
print("Model:", HF_IMAGE_MODEL, "Provider:", HF_PROVIDER)

client = InferenceClient(
    provider=HF_PROVIDER,
    api_key=HF_TOKEN,
    timeout=300,
)

prompts = [
    "Alex the young engineer arriving at construction site at sunrise, anime style, cinematic, no text",
    "Alex building foundation with workers, dramatic lighting, detailed construction, anime comic style, no text",
    "Alex on scaffolding working hard, sunset sky, expressive face, professional comic art, no text",
    "Alex tired but proud at construction site, evening light, cranes background, anime style, no text",
    "Alex looking at finished building, proud smile, sunset, cinematic comic illustration, no text"
]

os.makedirs("app/static/panels", exist_ok=True)
os.makedirs("app/static/exports", exist_ok=True)

for i, prompt in enumerate(prompts, 1):
    print(f"\n[{i}/5] Generating: {prompt[:50]}...")
    try:
        image = client.text_to_image(
            prompt,
            width=IMAGE_WIDTH,
            height=IMAGE_HEIGHT,
            model=HF_IMAGE_MODEL,
        )
        path = f"app/static/panels/panel_{i}.png"
        image.save(path)
        print(f"Saved {path}")
    except Exception as e:
        print(f"Failed panel {i}: {e}")
        print("Check internet — connect to phone hotspot if college WiFi blocks HF")
        time.sleep(5)
        continue

print("\nAll done! Check app/static/panels/ folder in explorer")