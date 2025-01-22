from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List

class QuoteResponse(BaseModel):
    id: str = Field(..., alias="_id")
    quote: str
    author: str
    tags: List[str]
    scraped_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

    @field_validator('tags', mode='before')
    @classmethod
    def clean_tags(cls, value):
        if isinstance(value, str):
            # Eliminar "Tags:" y espacios en blanco
            cleaned = value.replace("Tags:", "").strip()
            # Dividir por saltos de línea y filtrar strings vacíos
            tags = [tag.strip() for tag in cleaned.split('\n') if tag.strip()]
            return tags
        return value