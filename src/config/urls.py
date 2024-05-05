from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair

from issues.api import (
    IssuesAPI,
    IssuesRetrieveUpdateDeleteAPI,
    issues_close,
    issues_take,
    messages_api_dispatcher,
)
from users.api import UserListCreateAPI, UserRetrieveUpdateDeleteAPI, resend_activation_mail  #noqa

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Users
    path("users/", UserListCreateAPI.as_view()),
    path("users/activation/resendActivation", resend_activation_mail),
    path("users/<int:id>", UserRetrieveUpdateDeleteAPI.as_view()),
    # Issues
    path("issues/", IssuesAPI.as_view()),
    path("issues/<int:id>", IssuesRetrieveUpdateDeleteAPI.as_view()),
    path("issues/<int:id>/close", issues_close),
    path("issues/<int:id>/take", issues_take),
    # Messages
    path("issues/<int:issue_id>/messages", messages_api_dispatcher),
    # Authentication
    path("auth/token/", token_obtain_pair),
]
