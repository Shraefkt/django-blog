from django.db import models
from users.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Message(models.Model):
     sender = models.ForeignKey(User, related_name="sender",on_delete= models.CASCADE)
     reciever = models.ForeignKey(User, related_name="reciever",on_delete=models.CASCADE)
     msg_content = models.TextField()
     created_at = models.DateTimeField(default = timezone.now)

     def get_absolute_url(self):
          return reverse('message-sent')