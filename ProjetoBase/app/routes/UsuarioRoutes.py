from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session

from entidades.models import UsuarioPublico
from controllers import UsuarioController
from dependecies.dependencies import database

usuario_router = APIRouter()


# ----------------------------------------------------------------------------
# Schema específico do POST: recebe a senha além dos dados públicos.
# Aqui sim é o lugar de expor a senha (só na entrada; nunca na saída).
# ----------------------------------------------------------------------------
class UsuarioCreate(UsuarioPublico):
    usuario_senha: str = Field(min_length=6, max_length=255)


# GET — listar
@usuario_router.get("/usuarios", status_code=status.HTTP_200_OK)
def buscar_usuarios(db: Session = Depends(database.get_db)):
    try:
        return UsuarioController.buscar_usuarios(db)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# GET por id
@usuario_router.get("/usuarios/{usuario_id}", status_code=status.HTTP_200_OK)
def buscar_usuario(usuario_id: int, db: Session = Depends(database.get_db)):
    try:
        return UsuarioController.buscar_usuario_por_id(db, usuario_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# POST — criar (recebe senha)
@usuario_router.post("/usuarios", status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(database.get_db)):
    try:
        # Separa o schema público dos dados sensíveis
        dados_publicos = UsuarioPublico(**dados.model_dump(exclude={"usuario_senha"}))
        return UsuarioController.cadastrar_usuario(db, dados_publicos, dados.usuario_senha)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# PUT — atualizar (não mexe em senha)
@usuario_router.put("/usuarios/{usuario_id}")
def atualizar_usuario(
    usuario_id: int, dados: UsuarioPublico, db: Session = Depends(database.get_db)
):
    try:
        return UsuarioController.atualizar_usuario(db, usuario_id, dados)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# DELETE — remover
@usuario_router.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: int, db: Session = Depends(database.get_db)):
    try:
        UsuarioController.deletar_usuario(db, usuario_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )