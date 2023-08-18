from random import choices


def generate_invite_code() -> str:
    return "".join(choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))
