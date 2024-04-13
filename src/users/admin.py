from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(
    User
)  # создание на основе класса модели отобрадение в админпанели
class UserAdmin(admin.ModelAdmin):
    exclude = ["user_permissions", "groups"]  # удаляет строки в адм панели
    readonly_fields = (  # переносится вниз панели и не может изменяться админом #noqa
        "password",
        "date_joined",
        "last_login",
        "is_superuser",
        "email",
    )
