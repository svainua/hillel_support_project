import csv
import json
import random
import string

from django.http import Http404  # noqa
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render  # noqa
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from issues.models import Issue


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        # fields = ["id", "title", "body", "juniour_id"]    # выдает выборочные поля из модели    #noqa
        # exclude = ["id"] # выдает все поля, кроме указанного
        fields = "__all__"  # выдает все поля из модели

    # def validate(self, attrs):     # attrs - значения, которые приходят к нам в виде словаря. НАПОМНИТЬ ДИМЕ,КАК РАБОТАЕТ!!!   #noqa
    #     return attrs


@api_view()
def get_issues(request) -> Response:

    issues = Issue.objects.all()
    # results = [IssueSerializer(issue) for issue in issues]
    results = [IssueSerializer(issue).data for issue in issues]

    return Response(data={"results": results})

    # issues = Issue.objects.all()

    # results: list[dict] = [
    #     {
    #         "id": issue.id,
    #         "title": issue.title,
    #         "body": issue.body,
    #         "senior_id": issue.senior_id,
    #         "junior_id": issue.junior_id,
    #     }
    #     for issue in issues
    # ]

    # return Response(data={"results": results})


@api_view()
def retreive_issue(
    request, issue_id: int
) -> Response:  # выведение данных по значению Id в запросе в Postman
    instance = get_object_or_404(Issue, id=issue_id)
    # try:
    #     instance = Issue.objects.get(id=issue_id)
    # except Issue.DoesNotExist:     # На случай, если нет такого ID
    #     raise Http404()

    return Response(data={"results": IssueSerializer(instance).data})


@api_view(["POST"])
def create_issue(request) -> Response:
    try:
        payload: dict = json.loads(request.body)  # получаем данные из POST
    except json.decoder.JSONDecodeError:
        raise Exception("Request body is invalid")

    # трансформируем в dict, чтобы записать в issue.
    serializer = IssueSerializer(
        data=payload
    )  # пропускаем payload через валидатор
    serializer.is_valid(
        raise_exception=True
    )  # освободили себя от процесса валидации данных и передали его на уровень Модели наверх в класс Мета    #noqa

    issue = Issue.objects.create(
        **serializer.validated_data
    )  # распаковываем и записываем всё в Базу Данных

    # return Response(data={})
    # return Response(data=serializer.validated_data) # данные после валидации.
    return Response(
        data=IssueSerializer(issue).data
    )  # отображает данные после записи в БД


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
    path = "/Users/vladimirsaratovsky/Documents/GitHub/hillel_support_project/Oles.csv"  # noqa
    data = []
    result = []
    num = 1

    with open(path, newline="", encoding="utf-8") as csvfile:
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

        result.append(
            {
                "id": issue.id,
                "title": issue.title,
                "body": issue.body,
                "senior_id": issue.senior_id,
                "junior_id": issue.junior_id,
            }
        )

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


def post_issue(request: HttpRequest) -> JsonResponse:
    post_data = json.loads(request.body)

    issues = Issue.objects.create(
        title=post_data.get("title"),
        body=post_data.get("body"),
        senior_id=post_data.get("senior_id"),
        junior_id=post_data.get("junior_id"),
    )

    result = {
        "title": issues.title,
        "body": issues.body,
        "senior_id": issues.senior_id,
        "junior_id": issues.junior_id,
    }

    return JsonResponse(data=result)
