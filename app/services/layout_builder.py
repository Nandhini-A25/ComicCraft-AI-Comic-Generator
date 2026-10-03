from app.models import StoryResponse, ComicPanel


def build_comic_layout(story: StoryResponse, image_urls: list[str]) -> list[ComicPanel]:
    if len(story.panels) != len(image_urls):
        raise ValueError("Every story panel must have exactly one generated image.")

    return [
        ComicPanel(
            panel_number=panel.panel_number,
            title=panel.title,
            scene_description=panel.scene_description,
            caption=panel.caption,
            narration=panel.narration,
            dialogue=panel.dialogue,
            image_prompt=panel.image_prompt,
            image_url=image_urls[index],
        )
        for index, panel in enumerate(story.panels)
    ]
