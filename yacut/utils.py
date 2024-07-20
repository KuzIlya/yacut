import os
import json
from functools import wraps
from random import choice
from string import ascii_letters, digits

from .errors_handlers import UniquenessError

SHORT_ID_LENGTH = 6
MAX_COMBINES = (len(ascii_letters) + len(digits)) ** SHORT_ID_LENGTH
COUNTER_FILE = 'counter.json'


def load_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as file:
            data = json.load(file)
            return data.get('counter', 0)
    return 0


def save_counter(counter):
    with open(COUNTER_FILE, 'w') as file:
        json.dump({'counter': counter}, file)


counter = load_counter()


def counter_of_combines(func):
    """Декоратор для проверки уникальности строки."""
    generated_ids = set()

    @wraps(func)
    def wrapper(*args, **kwargs):
        global counter
        nonlocal generated_ids
        if counter == MAX_COMBINES:
            raise UniquenessError(
                'Были использованны все значения из 6 символов'
            )
        while True:
            if (result_id := func(*args, **kwargs)) not in generated_ids:
                generated_ids.add(result_id)
                counter += 1
                save_counter(counter)
                return result_id

    wrapper.counter = lambda: counter

    return wrapper


@counter_of_combines
def get_unique_short_id() -> str:
    """Функция для генерации случайных строк"""
    characters = ascii_letters + digits
    random_string = "".join(choice(characters) for _ in range(SHORT_ID_LENGTH))
    return random_string
