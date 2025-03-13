from fastapi import APIRouter, Response, Depends
from app.exceptions import ExistingUserExeption
from app.auth.auth import get_password_hash
from app.auth.schemas import SUserRegister
from app.users.dao import UsersDAO


router = APIRouter(prefix='/auth',
                   tags=['Авторизация'],)


@router.post('/register')
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise ExistingUserExeption
    hashed_password = get_password_hash(user_data.password)

    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)