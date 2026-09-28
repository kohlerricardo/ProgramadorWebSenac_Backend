from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models import Roles, RolesPublico


# ----------------------------------------------------------------------------
# LISTAR TODAS AS ROLES
# ----------------------------------------------------------------------------
def buscar_roles(db: Session) -> list[Roles]:
    try:
        return db.exec(select(Roles)).all()
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# BUSCAR ROLE PELO ID
# ----------------------------------------------------------------------------
def buscar_role_por_id(db: Session, role_id: int) -> Roles:
    try:
        role = db.get(Roles, role_id)
        if not role:
            raise KeyError(f"Role de ID {role_id} não encontrada.")
        return role
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# CADASTRAR ROLE
# ----------------------------------------------------------------------------
def cadastrar_role(db: Session, dados_entrada: RolesPublico) -> Roles:
    try:
        nova_role = Roles(**dados_entrada.model_dump())
        db.add(nova_role)
        db.commit()
        db.refresh(nova_role)
        return nova_role
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro nos dados informados, verifique e tente novamente.") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# ATUALIZAR ROLE
# ----------------------------------------------------------------------------
def atualizar_role(db: Session, role_id: int, dados_atualizados: RolesPublico) -> Roles:
    try:
        role = db.get(Roles, role_id)
        if not role:
            raise KeyError(f"Role de ID {role_id} não encontrada.")

        # Aplica só os campos enviados
        for key, value in dados_atualizados.model_dump(exclude_unset=True).items():
            setattr(role, key, value)

        db.add(role)
        db.commit()
        db.refresh(role)
        return role
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro de integridade nos dados informados.") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# DELETAR ROLE
# ----------------------------------------------------------------------------
def deletar_role(db: Session, role_id: int) -> None:
    try:
        role = db.get(Roles, role_id)
        if not role:
            raise KeyError(f"Role de ID {role_id} não encontrada.")

        db.delete(role)
        db.commit()
    except IntegrityError as e:
        # FK usuario_has_role pode estar apontando para esta role
        db.rollback()
        raise ValueError(
            "Não é possível excluir: existem usuários vinculados a esta role."
        ) from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e