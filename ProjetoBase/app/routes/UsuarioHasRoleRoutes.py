from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from entidades.models import UsuarioHasRole, UsuarioHasRolePublico
from controllers import UsuarioHasRoleController
from dependencies.dependencies import database

usuario_has_role_router = APIRouter()


# GET — listar todos os vínculos
@usuario_has_role_router.get(
    "/usuarios-has-role",
    response_model=list[UsuarioHasRole],
    status_code=status.HTTP_200_OK,
)
def buscar_vinculos(db: Session = Depends(database.get_db)):
    try:
        return UsuarioHasRoleController.buscar_vinculos(db)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# GET — vínculo específico (PK composta via path params)
@usuario_has_role_router.get(
    "/usuarios-has-role/{usuario_id}/{role_id}",
    response_model=UsuarioHasRole,
)
def buscar_vinculo(usuario_id: int, role_id: int, db: Session = Depends(database.get_db)):
    try:
        return UsuarioHasRoleController.buscar_vinculo(db, usuario_id, role_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# POST — criar vínculo
@usuario_has_role_router.post(
    "/usuarios-has-role",
    response_model=UsuarioHasRole,
    status_code=status.HTTP_201_CREATED,
)
def criar_vinculo(
    dados: UsuarioHasRolePublico, db: Session = Depends(database.get_db)
):
    try:
        return UsuarioHasRoleController.cadastrar_vinculo(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# DELETE — remover vínculo
@usuario_has_role_router.delete(
    "/usuarios-has-role/{usuario_id}/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deletar_vinculo(usuario_id: int, role_id: int, db: Session = Depends(database.get_db)):
    try:
        UsuarioHasRoleController.deletar_vinculo(db, usuario_id, role_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )