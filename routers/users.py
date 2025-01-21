### Users DB API ###

from fastapi import APIRouter, HTTPException, status, Depends
from db.models.user import User, UserDB
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from utils.search_user import search_user
from utils.auth_utils import get_current_user
from bson import ObjectId
from passlib.context import CryptContext



# Definición del contexto para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserDB):
    existing_user = search_user("email", user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe"
        )

    # Hash de la contraseña antes de almacenarla
    hashed_password = pwd_context.hash(user.password)

    try:
        user_dict = user.model_dump()
        user_dict["password"] = hashed_password  # Reemplaza la contraseña por su hash
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error al procesar los datos del usuario: {str(e)}"
        )

    user_dict.pop("id", None)

    try:
        inserted_id = db_client["users"].insert_one(user_dict).inserted_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al insertar el usuario en la base de datos: {str(e)}"
        )

    try:
        new_user = user_schema(db_client["users"].find_one({"_id": inserted_id}))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al recuperar el usuario creado: {str(e)}"
        )

    return new_user  # Retornar directamente el diccionario



@router.get("/", response_model=list[User])
async def users(_current_user: User = Depends(get_current_user)):
    try:
        users_data = db_client["users"].find()  
        return users_schema(users_data)  
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener usuarios: {str(e)}"
        )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str, _current_user: User = Depends(get_current_user)):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}
