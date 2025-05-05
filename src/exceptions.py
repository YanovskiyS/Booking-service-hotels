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

class RoomNotFoundHTTPException(BronirovanieException):
    status_code = 404
    detail = "Данного номера не существует"

class HotelNotFoundHTTPException(BronirovanieException):
    status_code = 404
    detail = "Данного отеля не существует"

class AllRoomsAreBookedHTTPException(BronirovanieException):
    status_code = 404
    detail = "Не осталось свободных номеров"

class IncorrectPasswordException(BronirovanieException):
    detail = "Пароль не верный"


class IncorrectPasswordHTTPException(BronirovanieException):
    status_code = 401
    detail = "Пароль не верный"

class UserNotFoundException(BronirovanieException):
    detail = "Данного пользователя не существует"

class UserWithThisEmailAlreadyHTTPExist(BronirovanieException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"