from sqlmodel import Field, SQLModel,Relationship
from enum import Enum
from typing import Optional

class CategoriaEquipamento(SQLModel, table=True):
    __tablename__="categoria_equipamento"
    categoria_id: int | None = Field(default=None,primary_key=True)
    categoria_descricao: str =Field(min_length=2,max_length=100)
    equipamentos : list["Equipamento"] = Relationship(back_populates="equipamento_categoria")


################################################################################################################################
class EnumEquipamento(str,Enum):
    DISPONIVEL='DISPONIVEL'
    RESERVADO='RESERVADO'
    EM_MANUTENCAO='EM_MANUTENCAO'
    INDISPONIVEL='INDISPONÍVEL'

class EquipamentoBase(SQLModel):
    equipamento_patrimonio : str  = Field(min_length=6, max_length=20)
    equipamento_descricao :str  = Field(max_length=255)
    equipamento_status_equipamento : EnumEquipamento = Field(default=EnumEquipamento.DISPONIVEL)
    equipamento_categoria_equipamento_id : int = Field(foreign_key="categoria_equipamento.categoria_id")

class Equipamento(EquipamentoBase, table=True):
    __tablename__="equipamento"
    equipamento_id : int | None = Field(default=None, primary_key=True)
    equipamento_categoria: CategoriaEquipamento | None = Relationship(back_populates="equipamentos")
class EquipamentoPublico(EquipamentoBase):
    pass

################################################################################################################################

