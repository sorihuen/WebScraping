### User schema ###
from datetime import datetime,  timezone

def user_schema(user) -> dict:
    """
    Convierte un documento MongoDB en un diccionario compatible con el modelo User.
    """
    return {
        "_id": str(user["_id"]) if user.get("_id") else None,
        "username": user.get("username", ""),
        "email": user.get("email", ""),
        "created_at": user.get("created_at", datetime.now(timezone.utc)),
    }


def users_schema(users) -> list:
    """
    Convierte una lista de documentos MongoDB en una lista de diccionarios compatibles con el modelo User.
    """
    return [user_schema(user) for user in users]
