from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Conexión MongoDB
client = MongoClient(os.environ["MONGO_URI"])

# Base de datos
db = client["ISIS2304D08202610"]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):

    comentarios = list(
        db["comentarios"].find(
            {"bar_id": bar_id},
            {"_id": 0}
        )
    )

    return comentarios


@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):

    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()

    db["comentarios"].insert_one(datos)

    return {'mensaje': 'Comentario guardado'}
