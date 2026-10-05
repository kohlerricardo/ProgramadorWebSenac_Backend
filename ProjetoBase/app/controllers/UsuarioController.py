from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models import Usuario, UsuarioPublico
from core.security import cria_hash_senha

# ----------------------------------------------------------------------------
# LISTAR USUÁRIOS
# ----------------------------------------------------------------------------
def buscar_usuarios(db: Session) -> list[Usuario]:
    try:
        return db.exec(select(Usuario)).all()
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# BUSCAR USUÁRIO PELO ID
# ----------------------------------------------------------------------------
def buscar_usuario_por_id(db: Session, usuario_id: int) -> Usuario:
    try:
        usuario = db.get(Usuario, usuario_id)
        if not usuario:
            raise KeyError(f"Usuário de ID {usuario_id} não encontrado.")
        return usuario
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# CADASTRAR USUÁRIO
# Recebe o schema público + a senha separadamente, para não expor
# o campo de senha no schema de entrada principal.
# ----------------------------------------------------------------------------
def cadastrar_usuario(db: Session, dados_entrada: UsuarioPublico, senha: str) -> UsuarioPublico:
    try:
        # Combina os dados públicos com a senha para construir a tabela
        print(f"senha->{senha}")
        novo_usuario = Usuario(**dados_entrada.model_dump(), usuario_senha=cria_hash_senha(senha))
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return novo_usuario
    except IntegrityError as e:
        # Mais comum: e-mail duplicado (índice UNIQUE em usuario_email)
        db.rollback()
        raise ValueError("E-mail já cadastrado ou dados inválidos.") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# ATUALIZAR USUÁRIO
# ----------------------------------------------------------------------------
def atualizar_usuario(
    db: Session, usuario_id: int, dados_atualizados: UsuarioPublico
) -> Usuario:
    try:
        usuario = db.get(Usuario, usuario_id)
        if not usuario:
            raise KeyError(f"Usuário de ID {usuario_id} não encontrado.")

        # Aplica só os campos enviados (a senha NÃO é alterada por esta rota)
        for key, value in dados_atualizados.model_dump(exclude_unset=True).items():
            setattr(usuario, key, value)

        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro de integridade. Verifique se o e-mail já existe.") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# DELETAR USUÁRIO
# ----------------------------------------------------------------------------
def deletar_usuario(db: Session, usuario_id: int) -> None:
    try:
        usuario = db.get(Usuario, usuario_id)
        if not usuario:
            raise KeyError(f"Usuário de ID {usuario_id} não encontrado.")

        db.delete(usuario)
        db.commit()
    except IntegrityError as e:
        # FK em emprestimo (solicitante/aprovador) e usuario_has_role
        db.rollback()
        raise ValueError(
            "Não é possível excluir: existem empréstimos vinculados a este usuário."
        ) from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e