from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from chat.models import Message, Thread


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "thread",
            "id",
            "sender",
            "text",
            "is_read",
            "created_at",
        )


class MessageCreateSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ("text",)


class ThreadCreateSerializer(ModelSerializer):
    class Meta:
        model = Thread
        fields = (
            "id",
            "participants",
            "created_at",
            "updated_at",
        )

    def validate_participants(self, participants):
        if len(participants) != 2:
            raise ValidationError("error : 2 participants only")
        return participants


class ThreadListSerializer(ModelSerializer):
    last_message = SerializerMethodField("get_last_message")

    class Meta:
        model = Thread
        fields = (
            "id",
            "participants",
            "created_at",
            "updated_at",
            "last_message",
        )

    def get_last_message(self, instance: Thread):
        return MessageSerializer(instance.thread_messages.last()).data


class RetrieveThreadSerializer(ModelSerializer):
    messages = SerializerMethodField("get_messages")

    class Meta:
        model = Thread
        fields = ("id", "participants", "created_at", "updated_at", "messages")

    def get_messages(self, instance: Thread):
        return MessageSerializer(instance.thread_messages, many=True).data
