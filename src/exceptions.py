from fastapi import HTTPException


class BronirovanieException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BronirovanieException):
    detail = "Обьект не найден"

class AllRoomsAreBookedException(BronirovanieException):
    detail = "Не осталось свободных номеров"

class UserWithThisEmailAlreadyExist(BronirovanieException):
    detail = "Пользователь с таким email уже существует"

class HotelNotFoundException(BronirovanieException):
    detail = "Данного отеля не существует"

class RoomNotFoundException(ObjectNotFoundException):
    detail = "Данной комнаты не существует"

class BronirovanieHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class RoomNotFoundHTTPException(BronirovanieHTTPException):
    status_code = 404
    detail = "Данного номера не существует"

class HotelNotFoundHTTPException(BronirovanieHTTPException):
    status_code = 404
    detail = "Данного отеля не существует"

class AllRoomsAreBookedHTTPException(BronirovanieHTTPException):
    status_code = 404
    detail = "Не осталось свободных номеров"

class IncorrectPasswordException(BronirovanieHTTPException):
    detail = "Пароль не верный"


class IncorrectPasswordHTTPException(BronirovanieHTTPException):
    status_code = 401
    detail = "Пароль не верный"

class UserNotFoundException(BronirovanieException):
    detail = "Данного пользователя не существует"

class UserWithThisEmailAlreadyHTTPExist(BronirovanieHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"

class EmailNotRegisteredException(BronirovanieException):
    detail = "Пользователдь не бы зарегестрирован"

class HotelIsNotExist(BronirovanieException):
    detail = ("Данного отеля не существует")

class ObjectAlreadyExistsException(BronirovanieException):
    detail = "Данный обьект уже существует"