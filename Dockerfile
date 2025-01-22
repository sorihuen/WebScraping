# Usar una imagen base ligera
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Variables de entorno para minimizar problemas de interacción en Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Para desarrollo, no copiamos el código aquí
# COPY . .

# Crear un usuario no root
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exponer el puerto que usará FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación con hot-reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
