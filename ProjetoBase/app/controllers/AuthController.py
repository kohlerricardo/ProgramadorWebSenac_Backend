# Importações básicas de sessão, SELECT e exceções do SQLAlchemy
from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models import Usuario,Roles,UsuarioHasRole
from core.security import verifica_senha,criar_token
def fazer_login(db:Session,email:str,password:str):
    try:
        usuario = db.exec(select(Usuario).where(Usuario.usuario_email==email)).first()
        senha = usuario is not None and verifica_senha(password,usuario.usuario_senha)
        if not senha:
            raise ValueError("Credenciais Inválidas")
        #Relação 1:N
        # statement = select(Roles.roles_descricao).where(usuario.role_id == Roles.roles_id)
        # papel = db.exec(statement).first()
        #Relação N:N
        statement =(
            select(Roles.roles_descricao).
            join(UsuarioHasRole,
                Roles.roles_id == UsuarioHasRole.usuario_has_role_role_id).
                where(Usuario.usuario_id == usuario.usuario_id)
        )
        papeis = db.exec(statement).all()

    except IntegrityError as e:
        raise ValueError("Credenciais Inválidas") from e
    token = criar_token(str(usuario.usuario_id),roles=papeis)
    
    return {
        "access_token":token,
        "token_type": "bearer"
    }