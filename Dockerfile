# Usamos la imagen oficial de Python 3.10 (versión ligera)
FROM python:3.10-slim

# Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero las dependencias
COPY requirements.txt .

# Instalamos las librerías
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de nuestro código (main.py, index.html, etc.)
COPY . .

# Exponemos el puerto por el que se comunicará FastAPI
EXPOSE 8000

# El comando que arrancará el servidor cuando se encienda el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]