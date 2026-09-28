from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models import (
    UsuarioHasRole,
    UsuarioHasRolePublico,
    Usuario,
    Roles,
)


# ----------------------------------------------------------------------------
# LISTAR TODOS OS VÍNCULOS (usuario x role)
# ----------------------------------------------------------------------------
def buscar_vinculos(db: Session) -> list[UsuarioHasRole]:
    try:
        return db.exec(select(UsuarioHasRole)).all()
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# BUSCAR UM VÍNCULO ESPECÍFICO
# Como a PK é composta (usuario_id, role_id), passamos uma TUPLA em db.get().
# ----------------------------------------------------------------------------
def buscar_vinculo(db: Session, usuario_id: int, role_id: int) -> UsuarioHasRole:
    try:
        vinculo = db.get(UsuarioHasRole, (usuario_id, role_id))
        if not vinculo:
            raise KeyError(
                f"Vínculo usuário {usuario_id} x role {role_id} não encontrado."
            )
        return vinculo
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# CADASTRAR VÍNCULO
# ----------------------------------------------------------------------------
def cadastrar_vinculo(
    db: Session, dados_entrada: UsuarioHasRolePublico
) -> UsuarioHasRole:
    try:
        # PASSO 1 — Integridade referencial: usuário existe?
        if not db.get(Usuario, dados_entrada.usuario_has_role_usuario_id):
            raise ValueError("Usuário informado não está cadastrado no sistema.")

        # PASSO 2 — Integridade referencial: role existe?
        if not db.get(Roles, dados_entrada.usuario_has_role_role_id):
            raise ValueError("Role informada não está cadastrada no sistema.")

        # PASSO 3 — Persiste o vínculo
        novo_vinculo = UsuarioHasRole(**dados_entrada.model_dump())
        db.add(novo_vinculo)
        db.commit()
        db.refresh(novo_vinculo)
        return novo_vinculo
    except IntegrityError as e:
        # PK composta duplicada -> este vínculo já existe
        db.rollback()
        raise ValueError("Este vínculo já existe ou os dados são inválidos.") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# DELETAR VÍNCULO
# ----------------------------------------------------------------------------
def deletar_vinculo(db: Session, usuario_id: int, role_id: int) -> None:
    try:
        vinculo = db.get(UsuarioHasRole, (usuario_id, role_id))
        if not vinculo:
            raise KeyError(
                f"Vínculo usuário {usuario_id} x role {role_id} não encontrado."
            )
        db.delete(vinculo)
        db.commit()
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e