from enum import StrEnum, auto
from functools import lru_cache
from typing import LiteralString


class Role(StrEnum):
    ADMIN = auto()
    SENIOR = auto()
    JUNIOR = auto()

    @classmethod
    @lru_cache(maxsize=1)
    def users(cls) -> list[str]:
        return [cls.SENIOR, cls.JUNIOR]

    @classmethod
    @lru_cache(maxsize=1)
    def users_values(cls) -> list[str]:
        return [cls.SENIOR.value, cls.JUNIOR.value]

    @classmethod
    @lru_cache(
        maxsize=1
    )  # максимальное кол-во элементов в этом кеше 1. Сохраняет результат. Этот метод будет вызываться каждый раз и результат будет неизменяемый. поэтому хэшируем #noqa
    def choices(cls) -> list[tuple[str, LiteralString]]:
        results = [(role.value, role.name.capitalize()) for role in cls]
        return results
