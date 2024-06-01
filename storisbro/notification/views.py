from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notification.tasks import send_notification
from .models import Notification
from authentication.models import User
from authentication.serializers import UserSerializer
from .serializers import NotificationSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


class SendNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        message = request.data.get('message')

        if not user_id or not message:
            return Response({'error': 'user_id and message are required'}, status=status.HTTP_400_BAD_REQUEST)

        send_notification.delay(user_id=user_id, message=message)
        return Response({'success': True}, status=status.HTTP_202_ACCEPTED)
    

class NotificationMainAPIView(APIView):
    # def get(self, request, uid):
    #     notification_model = Notification.objects.get(user__UID=uid) 
    #     serializer = NotificationSerializer(notification_model)
    #     return Response(serializer.data)
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class NotificationGetAPIView(APIView):
    def get(self, request, uid):
        notification_model = Notification.objects.get(user__UID=uid) 
        serializer = NotificationSerializer(notification_model, many=True)
        return Response(serializer.data)
    

class NotificationVKandEmail(APIView):
    def get(self, request, uid):
        notification_model = get_object_or_404(User, UID=uid)
        serializer = UserSerializer(notification_model)
        return Response(serializer.data)
    