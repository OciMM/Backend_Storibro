from django.urls import path
from .views import SendNotificationView

urlpatterns = [
    path('send-notification/', SendNotificationView.as_view(), name='send-notification'),
]