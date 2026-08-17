from sqlmodel import SQLModel, Field, Relationship
from entidades.Equipamento import Equipamento

class CategoriaEquipamentosBase(SQLModel):
    categoria_descricao: str =Field(min_length=2,max_length=100)
    equipamentos : list["Equipamento"] = Relationship(back_populates="categoria_equipamento")

class Categoria_Equipamento(CategoriaEquipamentosBase, table=True):
    # __tablename__="categoria_equipamento"
    categoria_id: int | None = Field(default=None,primary_key=True)

class CategoriaEquipamentosCreate(CategoriaEquipamentosBase):
    pass

class CategoriaEquipamentoPublic(CategoriaEquipamentosBase):
    categoria_id: int