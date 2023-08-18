from rest_framework.exceptions import ValidationError


def is_otp_valid(otp: str) -> bool:
    """
    Validates string as an otp format.
    """
    if not otp.isnumeric():
        raise ValidationError("otp must be numeric")
