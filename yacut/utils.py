from functools import wraps
from random import choice
from string import ascii_letters, digits

from sqlalchemy import func as sql_func

from .models import URLMap
from .errors_handlers import UniquenessError

SHORT_ID_LENGTH = 6
MAX_COMBINES = (len(ascii_letters) + len(digits)) ** SHORT_ID_LENGTH


def counter_of_combines(func):
    """Декоратор для проверки уникальности строки."""
    generated_ids = set()

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal generated_ids
        if (
            URLMap.query.filter(
                sql_func.char_length(URLMap.short) == 6
            ).count()
            == MAX_COMBINES
        ):
            raise UniquenessError(
                "Были использованны все значения из 6 символов"
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
    random_string = "".join(choice(characters) for _ in range(SHORT_ID_LENGTH))
    return random_string
