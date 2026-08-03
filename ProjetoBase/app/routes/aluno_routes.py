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
    # Função next retorna o próximo valor de uma sequência, neste caso, com a sequencia gerada através da palavra yield dentro da função next_index
    id = next(database.next_index())
    print(f"{id} - {parametro}")
    database.insert(id,parametro)
    