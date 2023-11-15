from rest_framework import serializers

from .models import User
from .services.validators import validate_otp, validate_phone


class ReferrerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
            "last_name",
        )


class UserSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=4, min_length=4, validators=(validate_otp,), write_only=True, required=False)
    referrer = serializers.StringRelatedField(read_only=True)
    invite_code = serializers.CharField(write_only=True)
    # referrals = serializers.RelatedField(read_only=True, queryset=User.objects.filter())
    referrals = serializers.SerializerMethodField("get_referrals", read_only=True)

    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "otp",
            "invite_code",
            "referrer",
            "referrals",
        )

        extra_kwargs = {
            "phone_number": {"validators": (validate_phone,)},
            "ReferrerSerializer": {"read_only": True},
        }

    def get_referrals(self, referrer):
        return ReferrerSerializer(User.objects.filter(referrer=referrer), many=True).data
