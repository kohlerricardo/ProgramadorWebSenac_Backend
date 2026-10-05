from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from entidades.models import Roles, RolesPublico
from controllers import RolesController
from dependencies.dependencies import database

roles_router = APIRouter()


# GET — listar
@roles_router.get("/roles", response_model=list[Roles], status_code=status.HTTP_200_OK)
def buscar_roles(db: Session = Depends(database.get_db)):
    try:
        return RolesController.buscar_roles(db)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# GET por id
@roles_router.get(
    "/roles/{role_id}", response_model=Roles, status_code=status.HTTP_200_OK
)
def buscar_role(role_id: int, db: Session = Depends(database.get_db)):
    try:
        return RolesController.buscar_role_por_id(db, role_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# POST — criar
@roles_router.post("/roles", response_model=Roles, status_code=status.HTTP_201_CREATED)
def criar_role(dados: RolesPublico, db: Session = Depends(database.get_db)):
    try:
        return RolesController.cadastrar_role(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# PUT — atualizar
@roles_router.put("/roles/{role_id}", response_model=Roles)
def atualizar_role(
    role_id: int, dados: RolesPublico, db: Session = Depends(database.get_db)
):
    try:
        return RolesController.atualizar_role(db, role_id, dados)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# DELETE — remover
@roles_router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_role(role_id: int, db: Session = Depends(database.get_db)):
    try:
        RolesController.deletar_role(db, role_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )