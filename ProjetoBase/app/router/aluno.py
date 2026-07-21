from fastapi import APIRouter
from database.db import DB
routes = APIRouter(prefix="/api",
                   tags=["CRUD","Alunos"])

db = DB()

@routes.get("/alunos")
def get_all_users():
    return db.retrieve_all()

@routes.get("/alunos/{id}")
def get_users(id:int):
    return db.retrieve(id)

@routes.post("/alunos")
def insert_users(pay:dict):
    print(pay)
    id = pay.get("id")
    db.insert(id,pay)

@routes.put("/alunos/{id}")
def update_users():
    pass

@routes.delete("/alunos/{id}")
def delete_users(id:int):
    print(db.delete(id))