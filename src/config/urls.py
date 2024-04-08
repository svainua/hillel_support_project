from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView  # noqa
from rest_framework_simplejwt.views import token_obtain_pair

from issues.api import (
    create_issue,
    create_poderevyanski_issue,
    create_random_issue,
    get_issues,
    get_poderevyanski_issue,
    post_issue,
    retreive_issue,
)
from users.api import create_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", get_issues),
    path("issues/create-random", create_random_issue),
    path("issues/oles", create_poderevyanski_issue),
    path("issues/get-oles", get_poderevyanski_issue),
    path("issues/post-issue", post_issue),
    path("issues/create-issue", create_issue),
    path("issues/<int:issue_id>", retreive_issue),
    # Authentication
    path("auth/token/", token_obtain_pair),
    # path("auth/token/", TokenObtainPairView.as_view()), #одинак с пред строк
    path("users/create", create_user),
]
