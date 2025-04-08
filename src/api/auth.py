from fastapi import APIRouter
from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd
from src.schemas.users import UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)

    new_user_data = UserAdd(email=data.email, first_name=data.first_name, last_name=data.last_name ,hashed_password=hashed_password)
    async with async_session_maker() as session:
        user = UsersRepository(session).get_one_or_none()
        if user:
            return {"status": "Пользователь с такимм дынными существует"}
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return  {"status": "Ok"}
