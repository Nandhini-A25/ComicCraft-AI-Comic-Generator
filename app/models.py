from typing import List
from pydantic import BaseModel, Field, field_validator


class ComicRequest(BaseModel):
    story_prompt: str = Field(min_length=3, max_length=2000)
    character_name: str = Field(default="Alex", min_length=1, max_length=80)
    setting: str = Field(default="enchanted forest", min_length=1, max_length=120)
    tone: str = Field(default="adventurous", min_length=1, max_length=80)
    art_style: str = Field(default="comic book", min_length=1, max_length=120)

    @field_validator("story_prompt", "character_name", "setting", "tone", "art_style")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value


class PanelOutline(BaseModel):
    panel_number: int = Field(ge=1)
    title: str
    scene_description: str
    image_prompt: str


class OutlineResponse(BaseModel):
    panels: List[PanelOutline] = Field(min_length=1)


class StoryPanel(BaseModel):
    panel_number: int = Field(ge=1)
    title: str
    scene_description: str
    caption: str
    narration: str
    dialogue: List[str] = Field(default_factory=list)
    image_prompt: str


class StoryResponse(BaseModel):
    panels: List[StoryPanel] = Field(min_length=1)


class ComicPanel(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    caption: str
    narration: str
    dialogue: List[str]
    image_prompt: str
    image_url: str


class ComicResult(BaseModel):
    comic_id: str
    title: str
    panels: List[ComicPanel]
    pdf_url: str
