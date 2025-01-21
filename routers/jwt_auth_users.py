
### jwt_auth_users ###

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from utils.search_user import search_user
from auth.login import LoginRequest, Token
from dotenv import load_dotenv
import os


# Cargar variables de entorno desde .env
load_dotenv()


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET_KEY = os.getenv("SECRET_KEY")

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])



@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    user_db = search_user("email", login_request.email)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no existe"
        )
    
    if not crypt.verify(login_request.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es válida"
        )
    
    access_token = {
        "sub": user_db.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    
    return {
        "access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "bearer"
    }