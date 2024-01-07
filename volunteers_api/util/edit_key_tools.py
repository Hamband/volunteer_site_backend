import volunteers_api.config as config
from random import choices as random_choices


def generate() -> str:
    return "".join(random_choices(population=config.edit_key_alphabet, k=config.edit_key_length))
