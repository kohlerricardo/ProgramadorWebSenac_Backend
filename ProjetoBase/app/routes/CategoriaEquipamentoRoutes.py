from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from entidades.models import CategoriaEquipamento, CategoriaEquipamentoPublico
from controllers import CategoriaEquipamentoController
from dependecies.dependencies import database

categoria_equipamento_router = APIRouter()


# GET — listar
@categoria_equipamento_router.get(
    "/categorias-equipamento",
    response_model=list[CategoriaEquipamento],
    status_code=status.HTTP_200_OK,
)
def buscar_categorias(db: Session = Depends(database.get_db)):
    try:
        return CategoriaEquipamentoController.buscar_categorias(db)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# GET por id
@categoria_equipamento_router.get(
    "/categorias-equipamento/{categoria_id}",
    response_model=CategoriaEquipamento,
    status_code=status.HTTP_200_OK,
)
def buscar_categoria(categoria_id: int, db: Session = Depends(database.get_db)):
    try:
        return CategoriaEquipamentoController.buscar_categoria_por_id(db, categoria_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# POST — criar
@categoria_equipamento_router.post(
    "/categorias-equipamento",
    response_model=CategoriaEquipamento,
    status_code=status.HTTP_201_CREATED,
)
def criar_categoria(
    dados: CategoriaEquipamentoPublico, db: Session = Depends(database.get_db)
):
    try:
        return CategoriaEquipamentoController.cadastrar_categoria(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# PUT — atualizar
@categoria_equipamento_router.put(
    "/categorias-equipamento/{categoria_id}",
    response_model=CategoriaEquipamento,
)
def atualizar_categoria(
    categoria_id: int,
    dados: CategoriaEquipamentoPublico,
    db: Session = Depends(database.get_db),
):
    try:
        return CategoriaEquipamentoController.atualizar_categoria(
            db, categoria_id, dados
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# DELETE — remover
@categoria_equipamento_router.delete(
    "/categorias-equipamento/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deletar_categoria(categoria_id: int, db: Session = Depends(database.get_db)):
    try:
        CategoriaEquipamentoController.deletar_categoria(db, categoria_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )