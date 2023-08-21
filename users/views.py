from .models import User
from .serializers import UserSerializer
# from .serializers import OnboardUserSerializer, AccountVerificationSerializer
from .services import generate_otp, generate_invite_code
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from django.core.cache import cache
from pprint import pprint
from http import HTTPStatus
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError as DRFValidationError
import time
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthenticatedOrCreateOrReadOnly

from rest_framework.authentication import TokenAuthentication


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    model = User
    permission_classes = (IsAuthenticatedOrCreateOrReadOnly, )

    def get_serializer_class(self):
        return UserSerializer

    def get_queryset(self):
        return User.objects.filter()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print("")
        # print(f"request.data = {request.data}")
        # print(f"serializer.data = {serializer.data}")
        # print("")

        # received_invite_code = serializer.validated_data.get('invite_code')  # TODO
        received_otp = serializer.validated_data.get('otp')

        user, created = User.objects.get_or_create(**serializer.data)
        print("")
        print(f"user = {user}")
        print(f"created = {created}")
        print("")

        if created:
            otp = generate_otp()
            user.otp = otp
            # user.objects.update_fields('otp')
            user.save()
            time.sleep(2)  # mock send_otp
            data = serializer(data=user)
            return Response(data, status=HTTPStatus.CREATED)

        if not received_otp:
            return Response(data='You must provide OTP', status=HTTPStatus.BAD_REQUEST)

        # print(f"user.otp = {user.otp}")
        # print(f"received_otp = {received_otp}")

        if user.otp != received_otp:
            return Response(data='Invalid OTP', status=HTTPStatus.BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        return Response(data={'token': str(token)}, status=HTTPStatus.OK)


    # @action(detail=False, methods=['post'])
    # def create_with_otp(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     phone_number = serializer.validated_data.get('phone_number')
    #     received_invite_code = serializer.validated_data.get('invite_code')
    #
    #     if User.objects.filter(phone_number=phone_number).exists():
    #         return Response(data='User already exists', status=HTTPStatus.BAD_REQUEST)
    #
    #     otp = generate_otp()
    #     invite_code = generate_invite_code()
    #     while User.objects.filter(invite_code=invite_code).exists():
    #         invite_code = generate_invite_code()
    #
    #     referrer = User.objects.filter(invite_code=received_invite_code).first()
    #
    #     User.objects.create_user(
    #         **serializer.data,
    #         invite_code=invite_code,
    #         referred_by=referrer,
    #         is_active=False
    #     )
    #
    #     return Response(data='otp is sent', status=HTTPStatus.OK)
    #
    # @action(detail=False, methods=['post'])
    # def activate_with_otp(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     phone_number = serializer.validated_data.get('phone_number')
    #     received_otp = request.data.get('otp')
    #
    #     user = get_object_or_404(User, phone_number=phone_number)
    #
    #     if received_otp == user.otp:
    #         user.is_active = True
    #         user.save()
    #         return Response(data="User is created", status=HTTPStatus.CREATED)
    #     else:
    #         return Response(data="Invalid OTP", status=HTTPStatus.BAD_REQUEST)



# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     # serializer_class = ListUserSerializer
#     serializer_class = OnboardUserSerializer
#     # permission_classes = [IsAuthenticated]
#     # http_method_names = ["get", "post", "patch", "delete"]
#
#     # def get_queryset(self):
#     #     user: User = self.request.user
#     #     if is_admin_user(user):
#     #         return super().get_queryset().all()
#     #     return super().get_queryset().filter(id=user.id)
#
#     # def get_serializer_class(self):
#     #     if self.action == "create":
#     #         return OnboardUserSerializer
#     #     if self.action in ["partial_update", "update"]:
#     #         return UpdateUserSerializer
#     #     return super().get_serializer_class()
#
#     # def get_permissions(self):
#     #     permission_classes = self.permission_classes
#     #     if self.action in ["create"]:
#     #         permission_classes = [AllowAny]
#     #     elif self.action in ["list", "retrieve", "partial_update", "update"]:
#     #         permission_classes = [IsAuthenticated]
#     #     elif self.action in ["destroy"]:
#     #         permission_classes = [IsAdmin]
#     #     return [permission() for permission in permission_classes]
#
#     # @extend_schema(
#     #     responses={
#     #         200: inline_serializer(
#     #             name='VerificationStatus',
#     #             fields={
#     #                 "success": serializers.BooleanField(default=True),
#     #                 "message": serializers.CharField(default="OTP sent for verification!")
#     #             }
#     #         ),
#     #     },
#     #     description="Sign up with a validate phone number. i.e. 08130303030 or +2348130303030"
#     # )
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"success": True, "message": "OTP sent for verification!"}, status=200)


# class AuthViewSet(viewsets.GenericViewSet):
#     """Auth viewsets"""
#
#     # serializer_class = EmailSerializer
#     # permission_classes = [IsAuthenticated]
#
#     # def get_permissions(self):
#     #     permission_classes = self.permission_classes
#     #     if self.action in ["initiate_password_reset", "create_password", "verify_account"]:
#     #         permission_classes = [AllowAny]
#     #     return [permission() for permission in permission_classes]
#
#     # @extend_schema(
#     #     responses={
#     #         200: inline_serializer(
#     #             name="AccountVerificationStatus",
#     #             fields={
#     #                 "success": serializers.BooleanField(default=True),
#     #                 "message": serializers.CharField(default="Acount Verification Successful"),
#     #             },
#     #         ),
#     #     },
#     # )
#     @action(
#         methods=["POST"],
#         detail=False,
#         serializer_class=AccountVerificationSerializer,
#         url_path="verify-account",
#     )
#     def verify_account(self, request, pk=None):
#         """Activate a user acount using the verification(OTP) sent to the user phone"""
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"success": True, "message": "Acount Verification Successful"}, status=200)
