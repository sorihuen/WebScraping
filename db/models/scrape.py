from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class Quote(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # Usado para la identificación en MongoDB
    quote: str = Field(..., description="Texto de la cita.")
    author: str = Field(..., description="Autor de la cita.")
    tags: str = Field(..., description="Etiqueta(s) asociada(s) a la cita.")
    scraped_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha y hora en que se extrajo la cita.")

    class Config:
        # Permite que el campo `_id` se mapee como `id` en lugar de `_id`
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
