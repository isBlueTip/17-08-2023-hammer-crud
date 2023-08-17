from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "phone_number",
            "email",
            "is_active",
            "referee",  # как назвать людей, кого привёл?
        )
        # read_only_fields = (
        #     ''
        # )


class CreateUserSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            "username",
            "phone_number",
            "email",
            "otp",
        )
        read_only_fields = ""
