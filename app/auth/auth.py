import uuid_utils
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from pydantic import EmailStr

from app.users.dao import UsersDAO
from app.config import settings
from app.exceptions import NoAccess

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.MAX_AGE_ACCESS_TOKEN) # 5 минут сделано для теста
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_WORD, settings.HASH_ALGORITHM
    ) 
    return encoded_jwt

def create_refresh_token() -> str:
    token = str(uuid_utils.uuid7())
    return token

async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if user and verify_password(password, user.hashed_password):
        return user