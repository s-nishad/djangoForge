import random
import string
import uuid


def generate_uuid() -> str:
    return uuid.uuid4().hex


def uuid_factory() -> str:
    return uuid.uuid4().hex


def get_random_string(length):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))


def get_random_int(start: int, end: int):
    return random.randint(start, end)