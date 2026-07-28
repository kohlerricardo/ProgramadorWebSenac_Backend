from fastapi import APIRouter
from db import db
from entidades.Aluno import Aluno

aluno_rotas = APIRouter()
database = db.Database()

@aluno_rotas.get("/alunos")
def get_all():
    return database.retrieve()

@aluno_rotas.post("/alunos")
def insert_aluno(parametro : dict):
    id = parametro.get("id")
    database.insert(id,parametro)
    