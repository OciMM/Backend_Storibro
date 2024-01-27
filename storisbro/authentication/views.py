import secrets

from rest_framework_simplejwt.views import TokenObtainPairView

from .tasks import user_created
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
import redis

from .models import User
from .serializers import UserLoginSerializer, UserProfileSerializer, UserCreateSerializer


class Home(TemplateView):
    template_name = "Home.html"


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class ObtainTokenView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Проверка наличия ключа 'user' в response.data
        user = response.data.get('user') if response.data else None
        print(user)
        if user and not user.get('is_active'):
            print("Я запускаюсь")
            return Response({'error': 'Аккаунт не активирован.'}, status=status.HTTP_401_UNAUTHORIZED)

        return response


class UserProfileAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        instance = serializer.save()

        confirmation(instance)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return response


@csrf_exempt
def confirmation(user):
    confirmation_code = secrets.token_urlsafe(6)
    redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    redis_connection.set(f"confirmation_code:{user.id}", confirmation_code)

    user_created.delay(user.id, confirmation_code)


@csrf_exempt
def activate_account(request, user_id, confirmation_code):
    user = get_object_or_404(User, id=user_id)

    redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    stored_code = redis_connection.get(f"confirmation_code:{user.id}")

    if stored_code.decode('utf-8') == confirmation_code:
        user.is_active = True
        user.save()
        redis_connection.delete(f"confirmation_code:{user.id}")
        return JsonResponse({'message': 'Аккаунт успешно активирован.'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Неверный код подтверждения.'}, status=status.HTTP_401_UNAUTHORIZED) 