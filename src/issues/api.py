import random
import string
import csv

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render  # noqa

from issues.models import Issue

# Create your views here.


def get_issues(request: HttpRequest) -> JsonResponse:
    # issues = Issue.objects.create()
    # issues = Issue.objects.update()
    # issues = Issue.objects.get()
    # issues = Issue.objects.delete()
    issues: list[Issue] = Issue.objects.all()

    results: list[dict] = [
        {
            "id": issue.id,
            "title": issue.title,
            "body": issue.body,
            "senior_id": issue.senior_id,
            "junior_id": issue.junior_id,
        }
        for issue in issues
    ]

    return JsonResponse(data={"results": results})


def _random_string(length: int = 10) -> str:
    return "".join(random.choice(string.ascii_letters) for i in range(length))


def create_random_issue(request: HttpRequest) -> JsonResponse:
    issue = Issue.objects.create(
        title=_random_string(20),
        body=_random_string(30),
        senior_id=1,
        junior_id=2,
    )

    result = {
        "id": issue.id,
        "title": issue.title,
        "body": issue.body,
        "senior_id": issue.senior_id,
        "junior_id": issue.junior_id,
    }

    return JsonResponse(data=result)


def create_poderevyanski_issue(request: HttpRequest) -> JsonResponse:
    path = "/Users/vladimirsaratovsky/Documents/GitHub/hillel_support_project/Oles.csv"
    data = []
    result = []
    num = 1

    with open(path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)

    for row in data[1:]:
        
        new_title = row[1] + str(num)

        issue = Issue.objects.create(
        title=new_title,
        body=row[0],
        senior_id=2,
        junior_id=1,
        )

        result.append({
            "id": issue.id,
            "title": issue.title,
            "body": issue.body,
            "senior_id": issue.senior_id,
            "junior_id": issue.junior_id,
        })

        num += 1

    return JsonResponse(data=result, safe=False)


def get_poderevyanski_issue(request: HttpRequest) -> JsonResponse:
    issues: list[Issue] = Issue.objects.all()

    results: list[dict] = [
        {
            "id": issue.id,
            "title": issue.title,
            "body": issue.body,
            "senior_id": issue.senior_id,
            "junior_id": issue.junior_id,
        }
        for issue in issues
    ]

    return JsonResponse(data={"results": results})
