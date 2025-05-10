from fastapi import HTTPException, Response
from passlib.context import CryptContext
import jwt
from datetime import datetime, timezone, timedelta


from src.config import settings
from src.exceptions import UserNotFoundException, IncorrectPasswordException, UserWithThisEmailAlreadyExist
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict):
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")

    async def login_user(self, data: UserRequestAdd):
            user = await self.db.users.get_user_with_hashed_password(
                email=data.email
            )
            if not user:
                raise UserNotFoundException()
            if not self.verify_password(data.password, user.hashed_password):
                raise IncorrectPasswordException()
            access_token = self.create_access_token({"user_id": user.id})
            return access_token

    async def register_user(self, data: UserRequestAdd):
        hashed_password = self.hash_password(data.password)

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

    async def get_one_or_none_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)