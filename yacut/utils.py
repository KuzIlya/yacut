from functools import wraps
from random import choice
from string import ascii_letters, digits

from .errors_handlers import UniquenessError

SHORT_ID_LENGTH = 6
MAX_COMBINES = (len(ascii_letters) + len(digits)) ** SHORT_ID_LENGTH


def counter_of_combines(func):
    """Декоратор для проверки уникальности строки."""
    counter = 0
    generated_ids = set()

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal counter, generated_ids
        if counter == MAX_COMBINES:
            raise UniquenessError(
                'Были использованны все значения из 6 символов'
            )
        while True:
            if (result_id := func(*args, **kwargs)) not in generated_ids:
                generated_ids.add(result_id)
                counter += 1
                return result_id
    return wrapper


@counter_of_combines
def get_unique_short_id() -> str:
    """Функция для генерации случайных строк"""
    characters = ascii_letters + digits
    random_string = "".join(choice(characters) for _ in range(SHORT_ID_LENGTH))
    return random_string
