from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import status

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.mixins import DestroyModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from helpers.permissions import is_participant
from chat.models import Message, Thread
from chat.api.serializers import (
    MessageSerializer,
    ThreadCreateSerializer,
    ThreadListSerializer,
    RetrieveThreadSerializer,
)


class ThreadView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = request.user.participants.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ThreadCreateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        if request.user.id not in serializer.data.get("participants"):
            raise ValidationError(
                "You can't create a thread without yourself as a participant."
            )
        if instance := self.get_thread(
            serializer.data.get("participants"), request.user
        ):
            return Response(
                ThreadCreateSerializer(instance).data, status=status.HTTP_200_OK
            )
        return self.create(request, *args, **kwargs)

    def get_thread(self, participants, user: User):
        thread_id = (
            user.participants.through.objects.filter(user_id__in=participants)
            .values("thread_id")
            .annotate(count=Count("user_id"))
            .filter(count=len(participants))
            .values_list("thread_id", flat=True)
            .order_by("thread_id")
            .first()
        )
        if thread_id is not None:
            return Thread.objects.filter(id=thread_id).first()

    def create(self, request, *args, **kwargs):
        serializer = ThreadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ThreadsByUser(RetrieveModelMixin, GenericAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(id=int(kwargs["pk"])).first().participants.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveThreadView(RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Thread.objects.all()
    serializer_class = RetrieveThreadSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if is_participant(request.user.id, instance):
            return self.retrieve(request, *args, **kwargs)
        return Response({"Permission denied": status.HTTP_403_FORBIDDEN})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if is_participant(request.user.id, instance):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"Permission denied": status.HTTP_403_FORBIDDEN})


class RetrieveMessageView(RetrieveAPIView, UpdateAPIView, CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data["thread"] = kwargs["pk"]
        request.data["sender"] = request.user.id
        if thread := Thread.objects.filter(id=int(kwargs["pk"])).first():
            if not is_participant(request.user.id, thread):
                return Response({"Permission denied": status.HTTP_403_FORBIDDEN})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        message = self.get_object()
        if (
            is_participant(request.user.id, message.thread)
            and request.user.id != message.sender.id
        ):
            message.is_read = True
            message.save()
        return Response(MessageSerializer(message).data, status=status.HTTP_200_OK)


class MessageListView(RetrieveModelMixin, GenericAPIView):
    queryset = Thread.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.thread_messages.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UnreadMessageView(ListModelMixin, GenericAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_thread = list(request.user.participants.values_list("id", flat=True))
        count = Message.objects.filter(
            Q(thread__in=user_thread) & Q(is_read=False) & ~Q(sender=request.user.id)
        ).count()

        return Response({"unread_message_count": count}, status=status.HTTP_200_OK)
