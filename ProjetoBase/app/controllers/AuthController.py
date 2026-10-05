# Importações básicas de sessão, SELECT e exceções do SQLAlchemy
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from entidades.models import Usuario,UsuarioHasRole,Roles,UsuarioAutenticado
from core.security import verifica_senha, criar_token


def fazer_login(db:Session,username:str, password:str):
    try:
        usuario = db.exec(select(Usuario).where(Usuario.usuario_email==username)).first()
        print(f"{usuario}")
        senha_ok = usuario is not None and verifica_senha(password,usuario.usuario_senha)
        if not senha_ok:
            raise ValueError("Credenciais inválidas.")
        # Busca Roles
        statement = (
            select(Roles.roles_descricao)
            .join(
                UsuarioHasRole, 
                Roles.roles_id == UsuarioHasRole.usuario_has_role_role_id
            )
            .where(UsuarioHasRole.usuario_has_role_usuario_id == usuario.usuario_id)
        )
        roles = db.exec(statement).all()
    except IntegrityError as e:
        raise ValueError("Credenciais inválidas.") from e
    

    token = criar_token(str(usuario.usuario_id),roles=roles)
    # Retorna token
    return {
        "acess_token":token,
        "token_type":"bearer"
    }
    

