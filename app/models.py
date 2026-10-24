"""Request and response models used by the notes API."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class NoteInput(BaseModel):
    """A note payload accepted when creating or replacing a note."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Text must not be empty.")
        return cleaned


class NoteResponse(BaseModel):
    """A note returned by the API."""

    id: str
    text: str
