from django.urls import path
from .views import SendNotificationView, NotificationMainAPIView

urlpatterns = [
    path('send-notification/', SendNotificationView.as_view(), name='send-notification'),
    path('send-notification/<str:uid>/', NotificationMainAPIView.as_view())
]