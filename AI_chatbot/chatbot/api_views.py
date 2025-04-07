from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatSession, ChatMessage
from django.contrib.auth.models import User
import uuid

class ChatSessionView(APIView):
    """Handles chat session creation and retrieval"""

    def post(self, request):
        """Create a new chat session"""
        user = request.user if request.user.is_authenticated else None
        session = ChatSession.objects.create(user=user, session_id=str(uuid.uuid4()))
        return Response({"session_id": session.session_id}, status=status.HTTP_201_CREATED)

    def get(self, request, session_id):
        """Retrieve chat history for a session"""
        try:
            session = ChatSession.objects.get(session_id=session_id)
            messages = session.messages.all().order_by("timestamp")
            chat_history = [{"sender": msg.sender, "message": msg.message, "timestamp": msg.timestamp} for msg in messages]
            return Response({"session_id": session.session_id, "chat_history": chat_history})
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

class ChatMessageView(APIView):
    """Handles sending messages and storing chat history"""

    def post(self, request, session_id):
        """Send a message to the chatbot and get a response"""
        try:
            session = ChatSession.objects.get(session_id=session_id)
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        user_message = request.data.get("message", "").strip()
        if not user_message:
            return Response({"error": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Store user message
        ChatMessage.objects.create(session=session, sender="user", message=user_message)

        # TODO: Integrate AI response here (Currently placeholder response)
        bot_response = f"You said: {user_message}"  
        
        # Store bot response
        ChatMessage.objects.create(session=session, sender="bot", message=bot_response)

        return Response({"user_message": user_message, "bot_response": bot_response}, status=status.HTTP_200_OK)
