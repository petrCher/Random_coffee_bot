from typing import Type


class RandomCoffeeError(Exception):
    eng: str
    ru: str

    def __init__(self, eng: str, ru: str) -> None:
        self.eng = eng
        self.ru = ru
        super().__init__(eng)


class ObjectNotFound(RandomCoffeeError):
    def __init__(self, obj: type, obj_id_or_name: int | str):
        super().__init__(
            f"Object {obj.__name__} {obj_id_or_name=} not found",
            f"Объект {obj.__name__}  с идентификатором {obj_id_or_name} не найден",
        )


class ValueError(RandomCoffeeError):
    def __init__(self, value: str):
        super().__init__(f"Value {value} is not valid", f"Значение {value} недопустимо")


class AlreadyExists(RandomCoffeeError):
    def __init__(self, obj: type, obj_id_or_name: int | str):
        super().__init__(
            f"Object {obj.__name__}, {obj_id_or_name=} already exists",
            f"Объект {obj.__name__} с идентификатором {obj_id_or_name=} уже существует",
        )


class ForbiddenAction(RandomCoffeeError):
    def __init__(self, type: Type):
        super().__init__(
            f"Forbidden action with {type.__name__}",
            f"Запрещенное действие с объектом {type.__name__}",
        )
