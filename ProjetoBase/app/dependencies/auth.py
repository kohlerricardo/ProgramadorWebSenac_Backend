
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
import jwt

from core.security import decodificar_token
from entidades.models import Usuario,UsuarioAutenticado
from dependencies.dependencies import database

bearer_scheme = HTTPBearer(auto_error=True)


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
                    db=Depends(database.get_db)):
    # cred_exc = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Credenciais inválidas.",
    #     headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = decodificar_token(creds.credentials)
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas.",
        headers={"WWW-Authenticate": "Bearer"})
    
    usuario = db.get(Usuario, int(payload["sub"]))

    if not usuario:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas.",
        headers={"WWW-Authenticate": "Bearer"})
    
    return UsuarioAutenticado(
        usuario_id=usuario.usuario_id,
        usuario_nome=f"{usuario.usuario_nome}",
        usuario_sobrenome=f"{usuario.usuario_sobrenome}",
        usuario_email=usuario.usuario_email,
        usuario_roles=payload.get("roles", [])
    )

def require_roles(*roles_necessarias: str):

    def _checker(user: UsuarioAutenticado = Depends(get_current_user)) -> UsuarioAutenticado:
        if not set(roles_necessarias) & set(user.usuario_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Requer uma das roles: {list(roles_necessarias)}.",
            )
        return user
    return _checker