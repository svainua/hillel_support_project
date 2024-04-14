from django.db.models import Q
from rest_framework import generics, serializers

from users.enums import Role

from .enums import Status
from .models import Issue


class IssueSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)
    junior = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # позволяет в атрибут юзера junior записывать того, кто приходит в request user  #noqa

    class Meta:
        model = Issue
        fields = "__all__"  # выдает все поля из модели

    def validate(self, attrs):
        attrs["status"] = Status.OPENED
        return attrs


class IssuesAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = IssueSerializer

    def get_queryset(self):
        # TODO Separate for each role
        user = self.request.user
        if user.role == Role.ADMIN:
            return Issue.objects.all()
        elif user.role == Role.SENIOR:
            return Issue.objects.filter(
                Q(senior=user) | Q(senior=None)
            )  # https://www.w3schools.com/django/django_queryset_filter.php   #noqa
        elif user.role == Role.JUNIOR:
            return Issue.objects.filter(junior=user)
        else:
            raise Exception("You don't have access to the DB")

    def post(self, request):  # Прописывание permission
        if request.user.role == Role.SENIOR:
            raise Exception("The role is Senior")
        return super().post(request)


class IssuesRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    lookup_url_kwarg = "id"

    def delete(self, request, *args, **kwargs):
        if request.user.role != Role.ADMIN:
            raise Exception("Only admin can delete Issue")
        return super().delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.role == Role.JUNIOR:
            raise Exception("Only Admin and Senior can change issue")
        return super().put(request, *args, **kwargs)
