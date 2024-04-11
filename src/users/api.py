import json

from django.contrib.auth import (
    get_user_model,  # импортирует класс Usera из любой директории проекта
)
from django.http import HttpRequest, JsonResponse

User = get_user_model()


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
