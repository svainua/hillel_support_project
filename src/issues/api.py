from django.db.models import Q
from rest_framework import generics, permissions, response, serializers  # noqa
from rest_framework.decorators import api_view, permission_classes  # noqa
from rest_framework.request import Request

from users.enums import Role

from .enums import Status
from .models import Issue, Message
from . import openapi


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
    

    @openapi.schemas.user_create
    def get(self, request, *args, **kwargs):
        """Get issues from the database"""
        return super().get(request, *args, **kwargs)


class IssuesAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = IssueSerializer

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == Role.ADMIN:
    #         return Issue.objects.all()
    #     elif user.role == Role.SENIOR:
    #         return Issue.objects.filter(
    #             Q(senior=user) | Q(senior=None)
    #         )  # https://www.w3schools.com/django/django_queryset_filter.php   #noqa
    #     elif user.role == Role.JUNIOR:
    #         return Issue.objects.filter(junior=user)
    #     else:
    #         raise Exception("You don't have access to the DB")

    def get_queryset(self):
        if self.request.user.role == Role.JUNIOR:
            return Issue.objects.filter(junior=self.request.user)
        elif self.request.user.role == Role.SENIOR:
            return Issue.objects.filter(
                Q(senior=self.request.user)
                | (Q(senior=None) & Q(status=Status.OPENED))
            )

        return Issue.objects.filter_by_participant(user=self.request.user)

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


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # автоматич вытяг юзера из request и контекста  #noqa
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())

    class Meta:
        model = Message
        fields = "__all__"

    def save(self):
        if (
            user := self.validated_data.pop("user", None)
        ) is not None:  # pop -вытянуть   := маржлвый оператор, создает объект в моменте самой операции  #noqa
            self.validated_data["user_id"] = user.id

        if (issue := self.validated_data.pop("issue", None)) is not None:
            self.validated_data["issue_id"] = issue.id

        return super().save()


@api_view(["PUT"])
def issues_close(request: Request, id: int):
    issue = Issue.objects.get(id=id)
    if request.user.role != Role.SENIOR:
        raise PermissionError("Only Senior can close issue")

    if issue.status != Status.IN_PROGRESS:
        return response.Response(
            {
                "message": "This issue is already closed or wasn't taken by the senior yet"  # noqa
            },
            status=422,
        )

    else:
        # issue = Issue.objects.update(id=id, status=Status.CLOSED)
        issue.status = Status.CLOSED
        issue.save()

    serializer = IssueSerializer(issue)
    return response.Response(serializer.data)


@api_view(["PUT"])
def issues_take(request: Request, id: int):
    issue = Issue.objects.get(id=id)
    if request.user.role != Role.SENIOR:
        raise PermissionError("Only Senior can take an issue")

    if (issue.status != Status.OPENED) or (issue.senior is not None):
        return response.Response(
            {"message": "Issue is not Opened or senior is set."},
            status=422,
        )

    else:
        issue.senior = request.user
        issue.status = Status.IN_PROGRESS
        issue.save()

    serializer = IssueSerializer(issue)
    return response.Response(serializer.data)


# MESSAGES
@api_view(["GET", "POST"])
def messages_api_dispatcher(request: Request, issue_id: int):
    if request.method == "GET":
        # messages = Message.objects.filter(
        #     Q(issue__id=issue_id,
        #       issue__junior=request.user,
        #       ) | Q(
        #           issue__id=issue_id,
        #           issue__senior=request.user)
        #     ).order_by("timestamp")
        messages = Message.objects.filter(
            Q(
                issue__id=issue_id,
            )
            & (
                Q(
                    issue__senior=request.user,
                )
                | Q(
                    issue__junior=request.user,
                )
            )
        ).order_by(
            "-timestamp"
        )  # -timestamp в постмане выводит наверх последние ссобщения #noqa
        serializer = MessageSerializer(messages, many=True)

        return response.Response(serializer.data)

    else:
        issue = Issue.objects.get(  # noqa
            id=issue_id
        )  # понимание, к кому привязываем наш месседж
        payload = request.data | {"issue": issue_id}  # объединяем дату с id
        serializer = MessageSerializer(
            data=payload, context={"request": request}
        )  # передаем в сериализаитор объединенную инфу  #noqa
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.validated_data)
