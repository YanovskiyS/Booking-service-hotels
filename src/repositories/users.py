from asyncpg import UniqueViolationError
from pydantic import EmailStr, BaseModel
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from src.exceptions import UserWithThisEmailAlreadyExist
from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalar_one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True)

    async def add_user(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        try:
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
        except IntegrityError:
            raise UserWithThisEmailAlreadyExist
        return self.mapper.map_to_domain_entity(model)
