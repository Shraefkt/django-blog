from django.urls import path
from messaging import views
from .views import MessageInboxView,MessageSentView,MessageCreateView

urlpatterns = [
    path('inbox/', MessageInboxView.as_view(),name = "message-inbox"),
    path('sent/',MessageSentView.as_view(),name = "message-sent"),
    path('message/new/',MessageCreateView.as_view(),name = "message-create")
]