from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair

from issues.api import IssuesAPI, IssuesRetrieveUpdateDeleteAPI
from users.api import UserListCreateAPI, UserRetrieveUpdateDeleteAPI

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", UserListCreateAPI.as_view()),
    path("users/<int:id>", UserRetrieveUpdateDeleteAPI.as_view()),
    path("issues/", IssuesAPI.as_view()),
    path("issues/<int:id>", IssuesRetrieveUpdateDeleteAPI.as_view()),
    # Authentication
    path("auth/token/", token_obtain_pair),
]
