from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from entidades.models import CategoriaEquipamento
from dependecies.dependencies import database
from controllers import CategoriaEquipamentoController 
categoria_equipamento_router = APIRouter()

@categoria_equipamento_router.get("/categorias",
                                  response_model=list[CategoriaEquipamento],
                                  status_code=status.HTTP_200_OK)
def listarCategorias(db: Session = Depends(database.get_db)):
    try:
        categorias = CategoriaEquipamentoController.buscar_all_categoria_equipamento(db)
        if not categorias:
            return []
        return categorias
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@categoria_equipamento_router.post("/categorias",status_code=status.HTTP_201_CREATED,response_model=CategoriaEquipamento)
def cadastrarCategoria(categoria: CategoriaEquipamento,db: Session = Depends(database.get_db)):  
        try:
            categoria_cadastrada = CategoriaEquipamentoController.cadastrar_categoria_equipamento(db,categoria)
            return categoria_cadastrada
        except RuntimeError as e :
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

        
@categoria_equipamento_router.put("/categorias/{categoria_id}",status_code=status.HTTP_200_OK)
def atualizarCategoria(
    categoria_id:int,
    categoria_data:CategoriaEquipamento,
    db: Session = Depends(database.get_db)
    ):
    try:
        return CategoriaEquipamentoController.atualizar_categoria(db, categoria_id, categoria_data)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    
@categoria_equipamento_router.delete("/categorias/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(categoria_id: int, 
                      db: Session = Depends(database.get_db)):
    try:
        CategoriaEquipamentoController.deletar_categoria(db, categoria_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
