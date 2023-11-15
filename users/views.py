import time
from http import HTTPStatus

from rest_framework import mixins, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .permissions import IsAuthenticatedOrCreateOrReadOnly
from .serializers import UserSerializer
from .services import generate_otp


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    permission_classes = (IsAuthenticatedOrCreateOrReadOnly,)
    queryset = User.objects.filter()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        received_invite_code = serializer.validated_data.pop('invite_code', None)
        received_otp = serializer.validated_data.get("otp")
        phone_number = serializer.validated_data.get("phone_number")

        print("")
        print(f"request.data = {request.data}")
        print(f"serializer.validated_data = {serializer.validated_data}")
        print("")

        user, created = User.objects.get_or_create(phone_number=phone_number)
        print("")
        print(f"user = {user}")
        print(f"created = {created}")
        print("")

        if created:
            otp = generate_otp()
            user.otp = otp
            # referrer = User.objects.get(invite_code=received_invite_code)

            if referrer := User.objects.filter(invite_code=received_invite_code).first():
                user.referrer = referrer
            user.save(update_fields=("otp", "referrer"))
            time.sleep(2)  # mock send_otp
            return Response("OTP has been sent to your phone", status=HTTPStatus.CREATED)

        if not received_otp:
            return Response(data="You must provide OTP", status=HTTPStatus.BAD_REQUEST)

        if user.otp != received_otp:
            return Response(data="Invalid OTP", status=HTTPStatus.BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        return Response(data={"token": str(token)}, status=HTTPStatus.OK)
