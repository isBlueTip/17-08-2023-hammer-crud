from random import choices
from time import sleep


def generate_otp() -> str:
    sleep(2)
    return "".join(choices("0123456789", k=4))
