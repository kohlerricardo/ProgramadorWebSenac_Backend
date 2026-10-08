# ============================================================================
# IMPORTAÇÕES
# ----------------------------------------------------------------------------
# Field       -> declara colunas, PKs, FKs, restrições (min_length, max_length...)
# SQLModel    -> classe base que une Pydantic (validação) + SQLAlchemy (ORM)
# Relationship-> cria vínculos entre tabelas (N:N, 1:N)
# Enum        -> enumeração nativa do Python (usada para campos de status)
# Optional    -> apenas para deixar claro quando um campo aceita None
# datetime    -> usado em campos de data/hora dos empréstimos
# ============================================================================
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class UsuarioLogin(BaseModel):
    email:str
    senha:str
class UsuarioLogado(BaseModel):
    id:int
    nome:str
    email:str
    #Relacionamento Perfil <-> Usuário N:N
    roles:list[str]
    #Relacionamento Perfil <-> Usário 1:N
    #role:str
# ============================================================================
# CATEGORIA DE EQUIPAMENTO
# ----------------------------------------------------------------------------
# Base  -> campos puros (sem tabela) usados para validação de entrada/saída
# Table -> a tabela real do banco (hereda os campos da Base)
# Publico -> o que a API expõe / recebe do cliente
# ============================================================================
class CategoriaEquipamentoBase(SQLModel):
    # Descrição da categoria: entre 2 e 100 caracteres, obrigatória
    categoria_descricao: str = Field(min_length=2, max_length=100)


class CategoriaEquipamento(CategoriaEquipamentoBase, table=True):
    # Nome exato da tabela no MySQL
    __tablename__ = "categoria_equipamento"

    # PK auto-incrementada (None quando ainda não foi persistida)
    categoria_id: int | None = Field(default=None, primary_key=True)

    # Relacionamento 1:N -> uma categoria tem vários equipamentos
    # back_populates aponta para o atributo correspondente em Equipamento
    equipamentos: list["Equipamento"] = Relationship(back_populates="equipamento_categoria")


class CategoriaEquipamentoPublico(CategoriaEquipamentoBase):
    # Só herda os campos válidos para o cliente (sem PK).
    # Usado como schema de entrada no POST/PUT e como schema de saída.
    pass


# ============================================================================
# EQUIPAMENTO
# ============================================================================
class EnumEquipamento(str, Enum):
    # Herdar de (str, Enum) faz o Pydantic/FastAPI serializar como string.
    # Estes valores precisam bater com o ENUM do MySQL, senão dá LookupError.
    DISPONIVEL    = 'DISPONIVEL'
    RESERVADO     = 'RESERVADO'
    EM_MANUTENCAO = 'EM_MANUTENCAO'
    INDISPONIVEL  = 'INDISPONÍVEL'


class EquipamentoBase(SQLModel):
    # Patrimônio é o identificador físico único
    equipamento_patrimonio: str = Field(min_length=6, max_length=20)

    # Descrição livre do equipamento
    equipamento_descricao: str = Field(max_length=255)

    # Status começa como DISPONIVEL por padrão
    equipamento_status_equipamento: EnumEquipamento = Field(default=EnumEquipamento.DISPONIVEL)

    # FK -> aponta para categoria_equipamento.categoria_id
    equipamento_categoria_equipamento_id: int = Field(
        foreign_key="categoria_equipamento.categoria_id"
    )


class Equipamento(EquipamentoBase, table=True):
    __tablename__ = "equipamento"

    # PK
    equipamento_id: int | None = Field(default=None, primary_key=True)

    # Relacionamento reverso com CategoriaEquipamento
    equipamento_categoria: CategoriaEquipamento | None = Relationship(
        back_populates="equipamentos"
    )

    # Relacionamento 1:N -> um equipamento pode ter vários empréstimos (histórico)
    emprestimos: list["Emprestimo"] = Relationship(back_populates="equipamento")


class EquipamentoPublico(EquipamentoBase):
    # Schema de entrada/saída. NÃO contém equipamento_id,
    # evitando "mass assignment" (cliente forçar a PK).
    pass


# ============================================================================
# ROLES (papéis/perfis de usuário)
# ============================================================================
class RolesBase(SQLModel):
    # Ex.: "ADMIN", "APROVADOR", "SOLICITANTE" (até 25 caracteres)
    roles_descricao: str = Field(max_length=25)


class Roles(RolesBase, table=True):
    __tablename__ = "roles"
    roles_id: int | None = Field(default=None, primary_key=True)

    # Relacionamento com a tabela de associação N:N
    usuarios_has_role: list["UsuarioHasRole"] = Relationship(back_populates="role")


class RolesPublico(RolesBase):
    pass


# ============================================================================
# USUARIO
# ============================================================================
class UsuarioBase(SQLModel):
    # Dados "públicos" (não inclui senha para não vazar por engano)
    usuario_nome: str = Field(max_length=100)
    usuario_sobrenome: str = Field(max_length=100)
    # Email é único no banco e opcional no schema
    usuario_email: str | None = Field(default=None, max_length=100, unique=True)


class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuario"
    usuario_id: int | None = Field(default=None, primary_key=True)

    # Senha NUNCA fica na Base -> só na tabela, e nunca deve ser retornada
    usuario_senha: str = Field(max_length=255)

    # Relacionamento N:N com Roles, via tabela intermediária
    usuarios_has_role: list["UsuarioHasRole"] = Relationship(back_populates="usuario")

    # IMPORTANTE: Emprestimo tem DUAS FKs para Usuario (solicitante e aprovador).
    # Sem o sa_relationship_kwargs apontando qual FK pertence a qual relação,
    # o SQLAlchemy não sabe desambiguar e lança AmbiguousForeignKeysError.
    emprestimos_solicitados: list["Emprestimo"] = Relationship(
        back_populates="solicitante",
        sa_relationship_kwargs={
            "foreign_keys": "[Emprestimo.emprestimo_solicitante_id]"
        },
    )
    emprestimos_aprovados: list["Emprestimo"] = Relationship(
        back_populates="aprovador",
        sa_relationship_kwargs={
            "foreign_keys": "[Emprestimo.emprestimo_aprovador_id]"
        },
    )


class UsuarioPublico(UsuarioBase):
    # Schema que a API expõe — sem senha.
    pass


# ============================================================================
# USUARIO_HAS_ROLE (associação N:N entre usuario e roles)
# ============================================================================
class UsuarioHasRoleBase(SQLModel):
    # As duas FKs
    usuario_has_role_usuario_id: int = Field(foreign_key="usuario.usuario_id")
    usuario_has_role_role_id: int = Field(foreign_key="roles.roles_id")


class UsuarioHasRole(UsuarioHasRoleBase, table=True):
    __tablename__ = "usuario_has_role"

    # Chave primária COMPOSTA: o par (usuario_id, role_id) é único.
    # Redeclaramos os campos aqui para marcar primary_key=True nos dois.
    usuario_has_role_usuario_id: int = Field(
        foreign_key="usuario.usuario_id", primary_key=True
    )
    usuario_has_role_role_id: int = Field(
        foreign_key="roles.roles_id", primary_key=True
    )

    # Relacionamentos reversos
    usuario: Usuario | None = Relationship(back_populates="usuarios_has_role")
    role: Roles | None = Relationship(back_populates="usuarios_has_role")


class UsuarioHasRolePublico(UsuarioHasRoleBase):
    pass


# 
# ============================================================================
# EMPRESTIMO
# ============================================================================
class EnumStatusEmprestimo(str, Enum):
    # Ciclo de vida do empréstimo
    PENDENTE   = 'PENDENTE'
    APROVADO   = 'APROVADO'
    RECUSADO   = 'RECUSADO'
    FINALIZADO = 'FINALIZADO'


class EmprestimoBase(SQLModel):
    # Quem pede o empréstimo (obrigatório)
    emprestimo_solicitante_id: int = Field(foreign_key="usuario.usuario_id")
    # Quem aprova/recusa (opcional, preenchido depois)
    emprestimo_aprovador_id: int | None = Field(
        default=None, foreign_key="usuario.usuario_id"
    )
    # Qual equipamento será emprestado
    emprestimo_equipamento_id: int = Field(foreign_key="equipamento.equipamento_id")
    # Texto justificando a demanda
    emprestimo_demanda: str
    # Parecer do aprovador (opcional)
    emprestimo_parecer: str | None = None
    # Status inicial = PENDENTE
    emprestimo_status_emprestimo: EnumStatusEmprestimo = Field(
        default=EnumStatusEmprestimo.PENDENTE
    )
    # Data prevista de devolução (opcional)
    emprestimo_data_devolucao_prevista: datetime | None = None


class Emprestimo(EmprestimoBase, table=True):
    __tablename__ = "emprestimo"
    emprestimo_id: int | None = Field(default=None, primary_key=True)

    # Datas controladas pelo sistema (não vêm do cliente):
    # default_factory = gerado no momento da criação do objeto
    emprestimo_data_solicitacao: datetime = Field(default_factory=datetime.utcnow)
    emprestimo_data_aprovacao: datetime | None = None
    emprestimo_data_devolucao: datetime | None = None

    # Relacionamentos — passamos o foreign_keys para desambiguar as duas FKs
    # que apontam para usuario (solicitante e aprovador).
    solicitante: Usuario | None = Relationship(
        back_populates="emprestimos_solicitados",
        sa_relationship_kwargs={
            "foreign_keys": "[Emprestimo.emprestimo_solicitante_id]"
        },
    )
    aprovador: Usuario | None = Relationship(
        back_populates="emprestimos_aprovados",
        sa_relationship_kwargs={
            "foreign_keys": "[Emprestimo.emprestimo_aprovador_id]"
        },
    )
    equipamento: Equipamento | None = Relationship(back_populates="emprestimos")


class EmprestimoPublico(EmprestimoBase):
    # Sem campos de data controlados pelo servidor nem PK.
    pass