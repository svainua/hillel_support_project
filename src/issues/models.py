from django.db import models
from django.db.models import Q

from users.models import User

ISSUE_STATUS_CHOICES = (
    (1, "Opened"),
    (2, "In progress"),
    (3, "Closed"),
)


class IssuesManager(
    models.Manager
):  # реализация паттерна репозиторий. как данные с какого-либо хранилища должны получаться   #noqa
    def filter_by_participant(self, user: User):
        return self.filter(Q(junior=user) | Q(senior=user))


class Issue(models.Model):
    title = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField(choices=ISSUE_STATUS_CHOICES)
    body = models.TextField(null=True)

    junior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="junior_issues"
    )  # rel_name позволит потом для юзера junior получить все его связанные issues  #noqa
    senior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="senior_issues", null=True
    )

    objects = IssuesManager()

    def __repr__(self) -> str:
        return f"Issue [{self.pk} {self.title[:10]}]"

    def __str__(self) -> str:
        return self.title[:10]


class Message(models.Model):
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)  автоматич обновл на уровне СУБД,каждый раз,когда вносятся изменения в таблицу   #noqa

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
