# ----------------------------------------------------------------------------
# APIRouter        -> agrupa rotas para serem incluídas no app principal
# Depends          -> injeta dependências (ex.: sessão do banco)
# status           -> constantes HTTP legíveis
# HTTPException    -> erro HTTP com status + detail
# Session          -> tipagem da sessão injetada
# ----------------------------------------------------------------------------
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from entidades.models import Equipamento, EquipamentoPublico
from controllers import EquipamentoController
from dependecies.dependencies import database

# Router sem prefixo/tags para ficar igual ao seu padrão
equipamento_router = APIRouter()


# ----------------------------------------------------------------------------
# GET /equipamentos — lista todos
# ----------------------------------------------------------------------------
@equipamento_router.get(
    "/equipamentos",
    response_model=list[Equipamento],   # resposta sempre no formato da tabela
    status_code=status.HTTP_200_OK,
)
def buscar_equipamentos(db: Session = Depends(database.get_db)):
    try:
        return EquipamentoController.buscar_equipamentos(db)
    except RuntimeError as e:
        # Erro de infraestrutura -> 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# ----------------------------------------------------------------------------
# GET /equipamentos/{id} — busca um específico
# ----------------------------------------------------------------------------
@equipamento_router.get(
    "/equipamentos/{equipamento_id}",
    response_model=Equipamento,
    status_code=status.HTTP_200_OK,
)
def buscar_equipamento(equipamento_id: int, db: Session = Depends(database.get_db)):
    try:
        return EquipamentoController.buscar_equipamento_por_id(db, equipamento_id)
    except KeyError as e:
        # Não encontrado -> 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# ----------------------------------------------------------------------------
# POST /equipamentos — cria
# Entrada: EquipamentoPublico (NÃO o modelo de tabela, para o cliente
# não conseguir injetar equipamento_id).
# ----------------------------------------------------------------------------
@equipamento_router.post(
    "/equipamentos",
    response_model=Equipamento,
    status_code=status.HTTP_201_CREATED,
)
def criar_equipamento(
    dados: EquipamentoPublico, db: Session = Depends(database.get_db)
):
    try:
        return EquipamentoController.cadastrar_equipamento(db, dados)
    except ValueError as e:
        # Regra de negócio violada (categoria inexistente etc.) -> 400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# ----------------------------------------------------------------------------
# PUT /equipamentos/{id} — atualiza
# ----------------------------------------------------------------------------
@equipamento_router.put(
    "/equipamentos/{equipamento_id}",
    response_model=Equipamento,
)
def atualizar_equipamento(
    equipamento_id: int,
    dados: EquipamentoPublico,
    db: Session = Depends(database.get_db),
):
    try:
        return EquipamentoController.atualizar_equipamento(db, equipamento_id, dados)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# ----------------------------------------------------------------------------
# DELETE /equipamentos/{id} — remove
# 204 significa "sucesso, sem corpo de resposta"
# ----------------------------------------------------------------------------
@equipamento_router.delete(
    "/equipamentos/{equipamento_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deletar_equipamento(equipamento_id: int, db: Session = Depends(database.get_db)):
    try:
        EquipamentoController.deletar_equipamento(db, equipamento_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        # FK impediu exclusão -> 400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )