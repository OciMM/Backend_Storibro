from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserAPIView(APIView):
    def get(self, request, pk):
        try:
            user_model = User.objects.get(pk=pk)
            serializer = UserSerializer(user_model)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=404)