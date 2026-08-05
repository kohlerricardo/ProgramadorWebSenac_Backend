from fastapi import APIRouter,HTTPException, status
from db import db
from entidades.Aluno import Aluno
from controllers.AlunoController import verifica_campos,inserir_aluno,buscar_todos
aluno_rotas = APIRouter()

@aluno_rotas.get("/alunos")
def get_all():
    return buscar_todos()

@aluno_rotas.post("/alunos",status_code=status.HTTP_201_CREATED)
def insert_aluno(parametro : Aluno):
    try:
        verifica_campos(parametro)
        inserir_aluno(parametro)
    except ValueError as error:
        raise HTTPException(
            status_code= status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail= f"{error}"
        )
    

    