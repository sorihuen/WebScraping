from fastapi import APIRouter, HTTPException
from db.client import db_client  
from db.models.scrape import Quote
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from bson import ObjectId

router = APIRouter(
    prefix="/scrape",
    tags=["scrape"],
    responses={404: {"message": "Not found"}}
)

@router.get("/")
def scrape_and_save(url: str):
    """
    Recibe una URL, hace scraping de la página de citas, y guarda la información en la base de datos MongoDB.
    """
    try:
        # Hacer la solicitud HTTP a la página
        response = requests.get(url)
        response.raise_for_status()

        # Analizar el contenido HTML
        soup = BeautifulSoup(response.content, "html.parser")

        # Extraer la información de las citas (esto depende de la estructura de la página)
        quotes = [quote.get_text().strip() for quote in soup.find_all("span", class_="text")]  # Extrae el texto de la cita
        authors = [author.get_text().strip() for author in soup.find_all("small", class_="author")]  # Extrae el autor
        tags = [tag.get_text().strip() for tag in soup.find_all("div", class_="tags")]  # Extrae las etiquetas

        # Crear una cita para cada entrada extraída y guardarla en MongoDB
        for quote_text, author, tag in zip(quotes, authors, tags):
            quote = Quote(
                quote=quote_text,
                author=author,
                tags=tag,
                scraped_at=datetime.now()
            )

            # Guardar la cita en MongoDB
            quotes_collection = db_client["quotes"]  # Cambia el nombre de la colección si es necesario
            result = quotes_collection.insert_one(quote.dict())

        return {"message": "Datos guardados correctamente en la base de datos."}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error en la solicitud HTTP: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar los datos: {str(e)}")
    


@router.get("/list")
def list_quotes():
    """
    Recupera todas las citas guardadas en la base de datos y las devuelve como una lista.
    """
    try:
        # Conectar a la colección de citas en MongoDB
        quotes_collection = db_client["quotes"]

        # Recuperar todas las citas de la base de datos y convertir `_id` a string
        quotes_data = quotes_collection.find()
        quotes = []
        for quote in quotes_data:
            quote["_id"] = str(quote["_id"])  # Convertir ObjectId a string
            quotes.append(Quote(**quote))  # Crear instancia del modelo Quote

        # Devolver las citas como una lista
        return {"quotes": quotes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recuperar los datos: {str(e)}")
    

@router.get("/{id}")
def get_quote_by_id(id: str):
    """
    Recupera una cita específica de la base de datos basada en su ID.
    """
    try:
        # Validar si el ID es un ObjectId válido
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="El ID proporcionado no es válido.")
        # Conectar a la colección de citas en MongoDB
        quotes_collection = db_client["quotes"]
        # Buscar la cita por ID
        quote_data = quotes_collection.find_one({"_id": ObjectId(id)})

        if not quote_data:
            raise HTTPException(status_code=404, detail="No se encontró la cita con el ID proporcionado.")
        # Convertir `_id` a string y devolver como instancia del modelo
        quote_data["_id"] = str(quote_data["_id"])
        return Quote(**quote_data)
    except HTTPException as http_exc:
        raise http_exc  # Relevantar errores HTTP definidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recuperar la cita: {str(e)}")