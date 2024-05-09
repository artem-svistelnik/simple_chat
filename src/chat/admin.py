from django.contrib import admin
from .models import Message, Thread


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("participants", "created_at", "updated_at")
    raw_id_fields = ("participants",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "created_at")
    list_filter = ("created_at",)
    search_fields = ("sender", "created_at")
    raw_id_fields = ("sender",)
