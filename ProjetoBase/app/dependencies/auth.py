from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, status, HTTPException
from dependencies.dependencies import database
from sqlmodel import Session
import jwt
from core.security import decodifica_token
from entidades.models import Usuario, UsuarioLogado

#poderia ser basic, digest, bearer
auth_scheme = HTTPBearer(auto_error=True)

def buscar_usuario_atual(credenciais:HTTPAuthorizationCredentials = Depends(auth_scheme),db: Session = Depends(database.get_db)):
    try:
        payload = decodifica_token(credenciais.credentials)
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Tempo excedido na sessão")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                             detail="Credenciais inválidas",
                             headers={"WWW-Authenticate":"Bearer"})
    usuario=db.get(Usuario,int(payload['sub']))
    if not usuario:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                        detail="Credenciais inválidas",
                        headers={"WWW-Authenticate":"Bearer"})
    return UsuarioLogado(
        id = usuario.usuario_id,
        nome = f"{usuario.usuario_nome} {usuario.usuario_sobrenome}",
        email= usuario.usuario_email,
        #Relacionamento Perfil <-> Usuário N:N
        roles=payload.get("roles",[])
    )

def verifica_permissao(*permissao:str):
    
    def _verificar(usuario:UsuarioLogado = Depends(buscar_usuario_atual)):
        if not set(permissao) & set(usuario.roles):
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado.Necessário perfil {list(permissao)}"
            )
        return usuario
    return _verificar
        