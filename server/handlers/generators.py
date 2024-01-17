import string
import random


def generate_invite_code(length: int = 4) -> str:
    """Функция случайной генерации кодов приглашений пользователей.

    :param length: Длина кода
    :returns: Сгенерированный код пользователя.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
