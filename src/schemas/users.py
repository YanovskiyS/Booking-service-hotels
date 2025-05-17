from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str


class UserWithHashedPassword(User):
    hashed_password: str
