
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from config.Config import settings
import jwt
pwd_context = CryptContext(schemes=['argon2'],deprecated="auto")

#senhas em texto limpo
def cria_hash_senha(senha:str):
    return pwd_context.hash(senha)
#comparativo de senhas
def verifica_senha(senha_informada:str,senha_banco:str):
    return pwd_context.verify(senha_informada,senha_banco)

#codificar o token
def criar_token(info:str,roles:list[str]):
    vence_em = datetime.now(timezone.utc)+timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MINUTES)
    payload = {
        "sub":info,
        "roles":roles,
        "exp":vence_em,
        "iss": settings.JWT_ISSUER
    }
    return jwt.encode(payload,settings.JWT_SECRET_KEY,settings.JWT_ALGORITHM)
#decodificar o token
def decodifica_token(token:str):
    #qualquer problema, lança excessão
    payload = jwt.decode(token,
                         settings.JWT_SECRET_KEY,
                         settings.JWT_ALGORITHM,
                         issuer=settings.JWT_ISSUER)
    return payload