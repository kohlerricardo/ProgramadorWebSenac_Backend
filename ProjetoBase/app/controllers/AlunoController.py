from entidades.Aluno import Aluno
from db.db import Database
database = Database()

def verifica_campos(aluno :Aluno):
    if not aluno.nome:
        raise ValueError("Nome Inválido informado")
    if "@" not in aluno.email:
        raise ValueError("Email Inválido informado")

def inserir_aluno(aluno :Aluno):
    # Função next retorna o próximo valor de uma sequência, neste caso, com a sequencia gerada através da palavra yield dentro da função next_index
    id = next(database.next_index())
    database.insert(id,aluno)
    
def buscar_todos():
    return database.retrieve()    

