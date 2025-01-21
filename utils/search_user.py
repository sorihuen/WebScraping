from db.models.user import UserDB
from db.schemas.user import user_schema
from db.client import db_client
from fastapi import HTTPException, status


from db.client import db_client
from db.models.user import UserDB

def search_user(field: str, key: str):
    try:
        user_dict = db_client.users.find_one({field: key})
        if not user_dict:
            return None
            
        # Asegurarse de que todos los campos requeridos estén presentes
        return UserDB(
            username=user_dict.get('username'),
            email=user_dict.get('email'),
            password=user_dict.get('password'),
            _id=str(user_dict.get('_id')),
            created_at=user_dict.get('created_at')
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar el usuario: {str(e)}"
        )