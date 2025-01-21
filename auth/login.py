from pydantic import BaseModel, EmailStr

# validan los datos que entran y salen del endpoint

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str