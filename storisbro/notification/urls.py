from django.urls import path
from .views import SendNotificationView, NotificationMainAPIView, NotificationVKandEmail

urlpatterns = [
    path('send-notification/', SendNotificationView.as_view(), name='send-notification'),
    path('send-notification/<str:uid>/', NotificationMainAPIView.as_view()),
    path('send-notification/vk_and_email/<str:uid>/', NotificationVKandEmail.as_view()),
]