from rest_framework import serializers

from .models import User
from .services.validators import validate_otp, validate_phone


class UserSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=4, min_length=4, validators=(validate_otp,), write_only=True, required=False)
    referred_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "phone_number",
            "email",
            "otp",
            "referred_by",
            # "referrer",  # как назвать людей, кого привёл?
        )

        extra_kwargs = {
            "username": {"validators": ()},  # Exclude username from uniqueness validation
            "phone_number": {"validators": (validate_phone,)},  # Exclude username from uniqueness validation
        }
