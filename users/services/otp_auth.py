from random import choices


def generate_otp() -> str:
    return "".join(choices("0123456789", k=4))
