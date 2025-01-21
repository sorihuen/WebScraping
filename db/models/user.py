   ### user model ###

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  
    username: str = Field(..., min_length=3, max_length=30, description="El nombre de usuario debe tener entre 3 y 30 caracteres.")
    email: EmailStr  # Valida que el correo electrónico tenga un formato correcto
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Fecha de creación del usuario.")

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }


class UserDB(User):
    email: str
    password: str 