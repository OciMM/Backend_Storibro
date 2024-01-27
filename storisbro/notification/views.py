from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notification.tasks import send_notification

class SendNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        message = request.data.get('message')

        if not user_id or not message:
            return Response({'error': 'user_id and message are required'}, status=status.HTTP_400_BAD_REQUEST)

        send_notification.delay(user_id=user_id, message=message)
        return Response({'success': True}, status=status.HTTP_202_ACCEPTED)