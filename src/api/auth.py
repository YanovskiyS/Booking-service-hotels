from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.database import async_session_maker
from src.exceptions import UserWithThisEmailAlreadyExist, IncorrectPasswordHTTPException
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserLogin
from src.schemas.users import UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login")
async def login_user(db: DBDep, data: UserLogin, response: Response):
    try:
        access_token = await AuthService(db).login_user(data)
    except IncorrectPasswordHTTPException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    hashed_password = AuthService().hash_password(data.password)

    new_user_data = UserAdd(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        hashed_password=hashed_password,
    )
    try:
        await db.users.add_user(new_user_data)
    except UserWithThisEmailAlreadyExist as err:
        raise HTTPException(status_code=409, detail=err.detail)
    await db.commit()

    return {"status": "Ok"}


@router.get("/me")
async def only_auth(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out"}
