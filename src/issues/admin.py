from django.contrib import admin

from .models import Issue, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "junior", "senior"]
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["user", "issue", "timestamp", "body"]
