from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from dependencies.dependencies import database
from entidades.models import UsuarioLogin,UsuarioAutenticado
from controllers.AuthController import fazer_login
from dependencies.auth import get_current_user 
auth_routes = APIRouter()


@auth_routes.post("/auth/login")
def login(userLogin: UsuarioLogin,db:Session = Depends(database.get_db)):
    try:
        info_login = fazer_login(db,userLogin.username,userLogin.password)
        return info_login
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))

@auth_routes.post("/auth/logout")
def logout():
    pass
@auth_routes.get("/auth/me")
def me(usuario:UsuarioAutenticado = Depends(get_current_user)):
    return usuario