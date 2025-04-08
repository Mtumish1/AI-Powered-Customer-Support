from rest_framework import generics
from rest_framework.response import Response
from .models import ChatMessage, ChatSession
from .serializers import ChatMessageSerializer, ChatSessionSerializer
from .ai_service import get_ai_service  # Import AI service layer

class ChatSessionListCreateView(generics.ListCreateAPIView):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer

class ChatMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def perform_create(self, serializer):
        chat_message = serializer.save()  # Save user message

        if chat_message.sender == 'user':
            ai_service = get_ai_service()  # Get AI model (Ollama or Claude)
            ai_reply = ai_service.generate_response(chat_message.message)  # AI-generated response
            
            ChatMessage.objects.create(
                session=chat_message.session,
                sender="bot",
                message=ai_reply
            )
