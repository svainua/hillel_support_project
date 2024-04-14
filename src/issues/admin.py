from django.contrib import admin

from .models import Issue, Message


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "junior", "senior"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["user", "timestamp", "body"]
