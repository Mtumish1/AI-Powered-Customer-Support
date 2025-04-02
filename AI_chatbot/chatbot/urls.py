from django.urls import path
from .views import ChatSessionListCreateView, ChatMessageListCreateView

urlpatterns = [
    path('sessions/', ChatSessionListCreateView.as_view(), name='chat-session-list'),
    path('messages/', ChatMessageListCreateView.as_view(), name='chat-message-list'),
]
