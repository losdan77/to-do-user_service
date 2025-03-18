from fastapi import APIRouter, Response, Depends
from app.auth.auth import authenticate_user, get_password_hash
from app.auth.dependecies import get_current_user
from app.exceptions import VerifyOldPasswordException
from app.users.dao import UsersDAO
from app.users.models import Users
from app.users.schemas import SChangePassword

router = APIRouter(prefix='/users',
                   tags=['Пользователи'],)


@router.post('/change_password')
async def change_password(user_data: SChangePassword,
                          current_user: Users = Depends(get_current_user)):
    verify_old_password = await authenticate_user(current_user['email'],
                                                  user_data.old_password)
    
    if not verify_old_password:
        raise VerifyOldPasswordException
    
    new_hashed_password = get_password_hash(user_data.new_password)

    await UsersDAO.update_by_id(current_user['id'],
                                hashed_password = new_hashed_password)
    return 'ok'


@router.get('/profile/{id}')
async def get_profile_by_id(profile_id: str):
    profile = None
    try:
        profile = await UsersDAO.find_one_or_none(id=profile_id)
    except:
        pass

    return profile
