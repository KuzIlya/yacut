from functools import wraps
from random import choice
from string import ascii_letters, digits

from sqlalchemy import func as sql_func

from .constants import MAX_COMBINES, SHORT_ID_LENGTH
from .models import URLMap
from .errors_handlers import UniquenessError


def counter_of_combines(func):
    """Декоратор для проверки уникальности строки."""
    generated_ids = set()

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal generated_ids
        if (
            URLMap.query.filter(
                sql_func.char_length(URLMap.short) == SHORT_ID_LENGTH
            ).count()
            == MAX_COMBINES
        ):
            raise UniquenessError(
                f"Использованны все значения из {SHORT_ID_LENGTH} символов"
            )
        while True:
            if (result_id := func(*args, **kwargs)) not in generated_ids:
                generated_ids.add(result_id)
                return result_id

    return wrapper


@counter_of_combines
def get_unique_short_id() -> str:
    """Функция для генерации случайных строк"""
    characters = ascii_letters + digits
    return "".join(choice(characters) for _ in range(SHORT_ID_LENGTH))
