from django.db import models
from users.models import User


class Issue(models.Model):
    title = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField()

    junior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="junior_issues"
    )  # rel_name позволит потом для юзера junior получить все его связанные issues
    senior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="senior_issues", null=True
    )

    def __repr__(self) -> str:
        return f"Issue [{self.pk} {self.title[:10]}]"


# first_issue: Issue | None = Issue.objects.first()
# instance: Issue = Issue.objects.get(id=1)

# issue: Issue = Issue.objects.get(id=1)
# issue.title
# issue.status
# issue.junior.password

# #messages = Message.objects.filter(issue_id=issue.id)  вместо этого, при помощи Джанго можно прописать следующее:
# issue.message_set


class Message(models.Model):
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)  автоматич обновл на уровне СУБД,каждый раз,когда вносятся изменения в таблицу

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
