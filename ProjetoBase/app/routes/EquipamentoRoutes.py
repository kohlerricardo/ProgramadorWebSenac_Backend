
from fastapi import APIRouter, Depends,status, HTTPException
from sqlmodel import Session
from entidades.models import Equipamento
from controllers import EquipamentoController
from dependecies.dependencies import database
from entidades.models import Equipamento

equipamento_router = APIRouter()

@equipamento_router.get("/equipamentos", 

                         status_code=status.HTTP_200_OK)
def buscar_equipamentos(db: Session = Depends(database.get_db)):
    try:
        equipamentos = EquipamentoController.buscar_equipamentos(db)
        return equipamentos
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

@equipamento_router.post("/equipamentos", 
                         response_model=Equipamento, 
                         status_code=status.HTTP_201_CREATED)
def criar_equipamento(dados: Equipamento, db: Session = Depends(database.get_db)):
    try:
        # Repassa a validação e a persistência para o controller
        return EquipamentoController.cadastrar_equipamento(db, dados)
        
    except ValueError as e:
        # Retorna HTTP 400 (Bad Request) se a categoria não existir ou houver conflito de dados
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    except RuntimeError as e:
        # Retorna HTTP 500 (Internal Server Error) se o banco estiver inacessível
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )
@equipamento_router.put("/equipamentos/{equipamento_id}", response_model=Equipamento)
def atualizar_equipamento(equipamento_id: int, dados: Equipamento, db: Session = Depends(database.get_db)):
    try:
        return EquipamentoController.atualizar_equipamento(db, equipamento_id, dados)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@equipamento_router.delete("/equipamentos/{equipamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_equipamento(equipamento_id: int, db: Session = Depends(database.get_db)):
    try:
        EquipamentoController.deletar_equipamento(db, equipamento_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))