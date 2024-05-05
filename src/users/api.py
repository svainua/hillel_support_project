import json  # noqa
import uuid  #noqa

from django.contrib.auth import (
    get_user_model,  # импортирует класс Usera из любой директории проекта
)
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, JsonResponse  # noqa
from rest_framework import generics, permissions, serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view

#from .services import send_user_activation_email, create_activation_key
from .services import Activator

from .enums import Role

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "role"]

    def validate_role(self, value: str) -> str:
        if value not in Role.users():
            raise ValidationError(
                f"Selected Role must be in {Role.users_values()}"
            )
        return value

    def validate(self, attrs: dict):
        """change the password for its hash"""
        attrs["password"] = make_password(attrs["password"])

        return attrs


class UserRegistrationPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "role"]


class UserListCreateAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )  # получаем сериализатор
        serializer.is_valid(raise_exception=True)  # валидируем данные
        self.perform_create(
            serializer
        )  # создаем со своим сериализатором данные

        #Function approach
        # activation_key: uuid.UUID = create_activation_key(email=serializer.data["email"])    #noqa
        # send_user_activation_email(email=serializer.data["email"], activation_key=activation_key)   #noqa

        # OOP approach
        activator_service = Activator(email=serializer.data["email"])
        activation_key = activator_service.create_activation_key()
        activator_service.send_user_activation_email(activation_key=activation_key)



        return Response(
            UserRegistrationPublicSerializer(serializer.validated_data).data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(
                serializer.data
            ),  # получить заголовки успеха
        )

    def get(self, request):
        queryset = (
            self.get_queryset()
        )  # возвращает всех юзеров в этот queryset
        serializer = UserSerializer(queryset)  #

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=self.get_success_headers(serializer.data),
        )


class UserRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "post", "put", "patch", "delete"]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "id"

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        password = request.data.get("password")
        if password:
            instance.set_password(password)
            instance.save()

        return JsonResponse(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        if not request.user.is_staff:
            raise PermissionError("Only admin can delete another user")
        return JsonResponse(serializer.data)


@api_view(http_method_names=["POST"])
def resend_activation_mail(request) -> Response:
    breakpoint()
    pass











# class UsersAPI(generics.ListCreateAPIView):
#     http_method_names = ["post"]
#     serializer_class = UserSerializer

#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = self.get_serializer(data=data)
#         if serializer.is_valid():
#             user = serializer.save()
#             password = data.get("password")
#             if password:
#                 user.set_password(password)
#                 user.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


# def create_user(request: HttpRequest) -> JsonResponse:
#     if request.method != "POST":
#         raise NotImplementedError("Only POST requests")

#     data: dict = json.loads(request.body)
#     user: User = User.objects.create_user(
#         **data
#     )  # в базе сохраняется зашифрованный пароль
#     # user: User = User.objects.create(**data)  # в базе сохраняется незашифрованный пароль  #noqa

#     # user.pk = None
#     # user.save()  эти 2 строки сделают нового пользователя. пока не используем  #noqa

#     # convert do dict
#     results = {
#         "id": user.id,
#         "email": user.email,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "role": user.role,
#         "is_active": user.is_active,
#     }

#     return JsonResponse(results)
