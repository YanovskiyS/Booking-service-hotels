
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

class HotelIsNotExist(BronirovanieException):
    detail = "Данного отеля не существует"
