from django.shortcuts import render, HttpResponse,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Message
from users.models import User
from django.views.generic import DetailView, ListView , CreateView

class MessageInboxView(ListView,LoginRequiredMixin):
    model = Message
    template_name = "messaging/message_inbox.html"
    context_object_name = "inbox_messages"
    ordering = ["created_at"]
    paginate_by = 10
    def get_queryset(self):
        user = self.request.user
        messages = Message.objects.filter(reciever=user).order_by("-created_at")
        return messages
class MessageSentView(ListView,LoginRequiredMixin):
    model = Message
    template_name = "messaging/message_sent.html"
    context_object_name = "sent_messages"
    ordering = ["created_at"]
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        messages = Message.objects.filter(sender=user).order_by("-created_at")
        return messages
class MessageCreateView(LoginRequiredMixin,CreateView):
    model = Message
    fields = ["reciever", "msg_content"]
    template_name = "messaging/message_create.html"
    def form_valid(self,form):
        form.instance.sender = self.request.user
        return super().form_valid(form)