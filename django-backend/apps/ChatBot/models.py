from django.db import models
from apps.Users.models import User
import uuid


class ChatHistory(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_history')
    model_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'chat_history'


class MessageHistory(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_history = models.ForeignKey(ChatHistory, on_delete=models.CASCADE, related_name='message_history')
    content = models.TextField()
    role = models.CharField(max_length=9)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message_history' 