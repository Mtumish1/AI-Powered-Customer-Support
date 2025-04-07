from django.urls import path
from .api_views import ChatSessionView, ChatMessageView

urlpatterns = [
    path('session/', ChatSessionView.as_view(), name="chat_session_create"),  # Create session
    path('session/<str:session_id>/', ChatSessionView.as_view(), name="chat_session_retrieve"),  # Get chat history
    path('chat/<str:session_id>/', ChatMessageView.as_view(), name="chat_interaction"),  # Send message
]
