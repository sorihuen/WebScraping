from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from db.models.user import User
from utils.search_user import search_user
from typing import Optional
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwtauth/login")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
        
    try:
        # Intentamos decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        # Verificamos si tenemos un username
        if not username:
            raise credentials_exception
            
        # Buscamos el usuario en la base de datos
        user = search_user("username", username)
        if not user:
            raise credentials_exception
            
        return user
        
    except JWTError:
        # Si hay cualquier error al decodificar el token
        raise credentials_exception