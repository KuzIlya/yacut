from random import choice
from string import ascii_letters, digits


def get_unique_short_id() -> str:
    characters = ascii_letters + digits
    random_string = "".join(choice(characters) for _ in range(6))
    return random_string
