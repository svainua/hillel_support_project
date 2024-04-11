import json

from django.contrib.auth import (
    get_user_model,  # импортирует класс Usera из любой директории проекта
)
from django.http import HttpRequest, JsonResponse
from rest_framework import generics, serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UsersAPI(generics.ListCreateAPIView):
    http_method_names = ["post"]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            password = data.get("password")
            if password:
                user.set_password(password)
                user.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


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


def create_user(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        raise NotImplementedError("Only POST requests")

    data: dict = json.loads(request.body)
    user: User = User.objects.create_user(
        **data
    )  # в базе сохраняется зашифрованный пароль
    # user: User = User.objects.create(**data)  # в базе сохраняется незашифрованный пароль  #noqa

    # user.pk = None
    # user.save()  эти 2 строки сделают нового пользователя. пока не используем

    # convert do dict
    results = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "is_active": user.is_active,
    }

    return JsonResponse(results)
