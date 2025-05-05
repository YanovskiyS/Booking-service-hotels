from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.exceptions import IncorrectPasswordException, UserNotFoundException, UserWithThisEmailAlreadyExist
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.services.base import BaseService
from fastapi import Response

class UserService(BaseService):
    async def login_user(self, data: UserRequestAdd, response: Response):
        async with async_session_maker() as session:
            user = await UsersRepository(session).get_user_with_hashed_password(
                email=data.email
            )
            if not user:
                raise UserNotFoundException()
            if not AuthService().verify_password(data.password, user.hashed_password):
                raise IncorrectPasswordException()
            access_token = AuthService().create_access_token({"user_id": user.id})
            response.set_cookie("access_token", access_token)
            return access_token

    async def register_user(self, data: UserRequestAdd):
        hashed_password = AuthService().hash_password(data.password)

        new_user_data = UserAdd(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            hashed_password=hashed_password,
        )
        try:
            await self.db.users.add_user(new_user_data)
        except UserWithThisEmailAlreadyExist:
            raise UserWithThisEmailAlreadyExist
        await self.db.commit()

    async def only_auth(self, user_id: UserIdDep):
        async with async_session_maker() as session:
            user = await UsersRepository(session).get_one_or_none(id=user_id)
            return user

    async def logout(self, response: Response):
        response.delete_cookie(key="access_token")
