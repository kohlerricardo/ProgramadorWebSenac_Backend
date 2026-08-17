from sqlmodel import Field, SQLModel,Relationship
from enum import Enum
from CategoriaEquipamentos import Categoria_Equipamento
class EnumEquipamento(str,Enum):
    DISPONIVEL='DISPONÍVEL'
    RESERVADO='RESERVADO'
    EM_MANUTENÇÃO='EM MANUTENÇÃO'
    INDISPONIVEL='INDISPONÍVEL'

class EquipamentoBase(SQLModel):
    equipamento_patrimonio : str  = Field(le=20,nullable=False)
    equipamento_descricao :str  = Field(le=255,nullable=False)
    equipamento_status_equipamento : EnumEquipamento

    equipamento_categoria_equipamento_id : int= Field(foreign_key="categoria_equipamento.categoria_id")
    equipamento_categoria: Categoria_Equipamento = Relationship(back_populates="categoria_equipamento")

class Equipamento(EquipamentoBase, table=True):
    equipamento_id : int | None = Field(default=None, primary_key=True)

