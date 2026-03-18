# 🐳 Docker RAG Assistant - Microservicio de IA

El objetivo de este proyecto es desplegar un microservicio utilizando Inteligencia Artificial Generativa y técnicas **RAG (Retrieval-Augmented Generation)**, todo ello contenerizado con Docker y orquestado con Docker Compose.

## 💡 Sobre el Proyecto (Originalidad)

Para aportar valor y originalidad al ejercicio, he decidido crear un **"Asistente Experto en Docker"**. 

El sistema RAG se alimenta de una base de conocimiento privada (`knowledge.txt`) que contiene documentación técnica avanzada sobre contenedores, volúmenes, redes y buenas prácticas. De esta forma, el chatbot no "alucina" con información de internet, sino que responde estrictamente basándose en los apuntes proporcionados.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.10+ y FastAPI
* **Inteligencia Artificial:** Google Gemini 2.5 Flash API (Google AI Studio)
* **Frontend:** Interfaz web tipo Chatbot (HTML/CSS/JS)
* **Infraestructura:** Docker y Docker Compose
* **Control de Versiones:** Git y GitHub

## 🚀 Cómo ejecutar el proyecto en local

Sigue estos pasos para arrancar el microservicio en tu máquina usando Docker:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/frxngv/rag-docker-microservice.git](https://github.com/frxngv/rag-docker-microservice.git)
cd rag-docker-microservice
```

### 2. Configurar la API Key
Por motivos de seguridad, la clave de la API de Gemini no está incluida en el repositorio.
1. Crea un archivo llamado `.env` en la raíz del proyecto.
2. Añade tu clave de Google AI Studio con el siguiente formato:
   ```text
   GEMINI_API_KEY=tu_clave_secreta_aqui
   ```

### 3. Levantar la infraestructura con Docker Compose
Asegúrate de tener Docker ejecutándose en tu equipo y lanza el siguiente comando:
```bash
docker-compose up -d --build
```
*Este comando descargará la imagen base de Python, instalará las dependencias necesarias (`fastapi`, `google-generativeai`, etc.), montará el volumen con la base de conocimiento y expondrá el puerto 8000.*

### 4. Acceder al Chatbot
Una vez que el contenedor esté en ejecución, abre tu navegador web y visita:
👉 **http://localhost:8000**

## 🏗️ Arquitectura y Volúmenes

El archivo `docker-compose.yml` está configurado para manejar:
* **Variables de Entorno:** Inyecta de forma segura el archivo `.env`.
* **Volúmenes (Bind Mounts):** El archivo `knowledge.txt` está montado como un volumen (`./knowledge.txt:/app/knowledge.txt`). Esto permite actualizar la base de conocimiento del chatbot en tiempo real sin necesidad de reconstruir la imagen de Docker.
