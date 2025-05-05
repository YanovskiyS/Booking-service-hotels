from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.database import async_session_maker
from src.exceptions import UserWithThisEmailAlreadyExist, UserWithThisEmailAlreadyHTTPExist
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd
from src.schemas.users import UserAdd
from src.services.auth import AuthService
from src.services.users import UserService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response):
    access_token = await UserService().login_user(data, response)
    return {"access_token": access_token}


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        await UserService(db).register_user(data)
    except UserWithThisEmailAlreadyExist:
        raise UserWithThisEmailAlreadyHTTPExist

    return {"status": "Ok"}


@router.get("/me")
async def only_auth(user_id: UserIdDep):
    user = await UserService().only_auth(user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    await UserService().logout(response)
    return {"message": "Logged out"}
