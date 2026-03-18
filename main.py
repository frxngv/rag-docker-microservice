import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Cargar la clave secreta desde el archivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("¡Cuidado! No se encontró GEMINI_API_KEY en el archivo .env")

# 2. Configurar la conexión con Google Gemini 2.5 Flash
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. Iniciar API con FastAPI
app = FastAPI(title="RAG Microservice - Experto en Docker")

# 4. Cargar base de conocimiento en memoria
try:
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        knowledge_base = f.read()
except FileNotFoundError:
    knowledge_base = "Error: No se encontró el archivo knowledge.txt"

# 5. Definir la estructura de la pregunta que recibiremos de la web
class Question(BaseModel):
    text: str

# 6. Crear el endpoint /ask 
@app.post("/ask")
async def ask_question(question: Question):
    try:
        prompt = f"""
        Eres un ingeniero experto en Docker. Tu misión es responder a la pregunta del usuario utilizando ÚNICAMENTE la información proporcionada en el siguiente contexto.
        Si la respuesta no está en el contexto, di amablemente: "Lo siento, mi base de conocimiento no contiene esa información." No inventes nada.

        Contexto privado:
        {knowledge_base}

        Pregunta del usuario: {question.text}
        """
        
        # Enviar el prompt a Gemini y devolver la respuesta
        response = model.generate_content(prompt)
        return {"answer": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 7. Endpoint para servir la página web del Chatbot
@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")