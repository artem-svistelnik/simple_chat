from django.urls import path
from .api import views

app_name = "chat"

urlpatterns = [
    path("threads/", views.ThreadView.as_view(), name="threads"),
    path("threads/<pk>/", views.RetrieveThreadView.as_view(), name="thread_detail"),
    path("threads/user/<pk>/", views.ThreadsByUser.as_view(), name="thread_by_user"),
    path(
        "messages/unread/",
        views.UnreadMessageView.as_view(),
        name="unread_messages_count",
    ),
    path(
        "messages/threads/<pk>/",
        views.MessageListView.as_view(),
        name="thread_messages",
    ),
    path("messages/<pk>/", views.RetrieveMessageView.as_view(), name="create_message"),
]
