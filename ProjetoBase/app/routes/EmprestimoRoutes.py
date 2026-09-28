from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from entidades.models import Emprestimo, EmprestimoPublico
from controllers import EmprestimoController
from dependecies.dependencies import database

emprestimo_router = APIRouter()


# GET — listar
@emprestimo_router.get(
    "/emprestimos", response_model=list[Emprestimo], status_code=status.HTTP_200_OK
)
def buscar_emprestimos(db: Session = Depends(database.get_db)):
    try:
        return EmprestimoController.buscar_emprestimos(db)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# GET por id
@emprestimo_router.get(
    "/emprestimos/{emprestimo_id}",
    response_model=Emprestimo,
    status_code=status.HTTP_200_OK,
)
def buscar_emprestimo(emprestimo_id: int, db: Session = Depends(database.get_db)):
    try:
        return EmprestimoController.buscar_emprestimo_por_id(db, emprestimo_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# POST — criar (dispara reserva do equipamento)
@emprestimo_router.post(
    "/emprestimos",
    response_model=Emprestimo,
    status_code=status.HTTP_201_CREATED,
)
def criar_emprestimo(dados: EmprestimoPublico, db: Session = Depends(database.get_db)):
    try:
        return EmprestimoController.cadastrar_emprestimo(db, dados)
    except ValueError as e:
        # Ex.: equipamento indisponível, solicitante inexistente -> 400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# PUT — atualizar (aprovação/finalização, com efeitos colaterais)
@emprestimo_router.put("/emprestimos/{emprestimo_id}", response_model=Emprestimo)
def atualizar_emprestimo(
    emprestimo_id: int,
    dados: EmprestimoPublico,
    db: Session = Depends(database.get_db),
):
    try:
        return EmprestimoController.atualizar_emprestimo(db, emprestimo_id, dados)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# DELETE — remover
@emprestimo_router.delete(
    "/emprestimos/{emprestimo_id}", status_code=status.HTTP_204_NO_CONTENT
)
def deletar_emprestimo(emprestimo_id: int, db: Session = Depends(database.get_db)):
    try:
        EmprestimoController.deletar_emprestimo(db, emprestimo_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )