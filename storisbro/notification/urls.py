from django.urls import path
from .views import SendNotificationView, NotificationMainAPIView, NotificationVKandEmail, NotificationGetAPIView

urlpatterns = [
    path('send-notification/', SendNotificationView.as_view(), name='send-notification'),
    path('send-notification/message/', NotificationMainAPIView.as_view()),
    path('send-notification/message/<str:uid>/', NotificationGetAPIView.as_view()),
    path('send-notification/vk_and_email/<str:uid>/', NotificationVKandEmail.as_view()),
    # path('send-notification/bulk-notifications/', BulkNotificationCreateAPIView.as_view(), name='bulk-notifications'),
]