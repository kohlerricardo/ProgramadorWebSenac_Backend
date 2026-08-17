from fastapi import FastAPI, Depends, HTTPException, status
from routes import aluno_routes
from dependecies.database import database
from entidades.CategoriaEquipamentos import Categoria_Equipamento, CategoriaEquipamentosCreate,CategoriaEquipamentoPublic
from sqlmodel import Session,select

app = FastAPI(
    title="Minha API",
    description="API de exemplo com FastAPI",
    version="1.0.0"
)
app.include_router(aluno_routes.aluno_rotas)

@app.get("/categorias",response_model=list[Categoria_Equipamento])
def listarCategorias(db: Session = Depends(database.get_db)):
    categorias = db.exec(select(Categoria_Equipamento)).all()
    return categorias

@app.post("/categorias",status_code=status.HTTP_201_CREATED,response_model=CategoriaEquipamentoPublic)
def cadastrarCategoria(categoria: CategoriaEquipamentosCreate,db: Session = Depends(database.get_db)):  
        newCategoria = Categoria_Equipamento.model_validate(categoria)
        db.add(newCategoria)
        db.commit()
        db.refresh(newCategoria)
        return newCategoria
@app.put("/categorias/{categoria_id}",status_code=status.HTTP_202_ACCEPTED)
def atualizarCategoria(
    categoria_id:int,
    db: Session = Depends(database.get_db)
    )->None:
        categoria = db.get(Categoria_Equipamento,categoria_id)
        print(categoria)
        if not categoria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria Não encontrada")
        
    
@app.delete("/categorias/{categoria_id}",status_code=status.HTTP_204_NO_CONTENT)
def atualizarCategoria(
    categoria_id:int,
    db: Session = Depends(database.get_db)
    )->None:
        categoria = db.get(Categoria_Equipamento,categoria_id)
        print(categoria)
        if not categoria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria Não encontrada")
        db.delete(categoria)
        db.commit()
