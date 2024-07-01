import secrets

from rest_framework_simplejwt.views import TokenObtainPairView

from .tasks import user_created, password_change_code, email_change_code
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
import redis
from django.contrib.auth.views import LoginView
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

import random
import string

from .models import User
from .serializers import UserLoginSerializer, UserProfileSerializer, UserCreateSerializer, UserSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


class Home(TemplateView):
    template_name = "Home.html"


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class BannedUserAPIView(UpdateAPIView):
    """Блокирова пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAPIView(APIView):
    def get(self, request):
        user_model = User.objects.all()
        serializer = UserSerializer(user_model, many=True)
        return Response(serializer.data)
    

class UserOneAPIView(APIView):
    def get(self, request, pk):
        user_model = User.objects.get(pk=pk)
        serializer = UserSerializer(user_model)
        return Response(serializer.data)


class ObtainTokenView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    # @method_decorator(ratelimit(key='user_or_ip', rate='5/m'))
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
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # def get(self, request, *args, **kwargs):
    #     token = request.auth
    #     print(f"Received token: {token}")
    #     return Response({"message": "Your response message"}, status=status.HTTP_200_OK)

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        else:
            raise exceptions.NotAuthenticated("User is not authenticated.")

    def perform_update(self, serializer):
        instance = serializer.save()

        confirmation(instance)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return response


class ChangeProfileData(APIView):
    """Класс для изменения данных профиля"""
    def patch(self, request, pk):
        instance = User.objects.get(pk=pk)
        serializer = UserProfileSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AllEmailUsersAPIView(APIView):
    def post(self, request):
        email_to_check = request.data.get('email', None)

        if email_to_check is not None:
            user_exists = User.objects.filter(email=email_to_check).exists()
            return Response({'exists': user_exists}, status=status.HTTP_200_OK)

        return Response({'error': 'Не указана почта для проверки'}, status=status.HTTP_400_BAD_REQUEST)


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
    

@csrf_exempt
def confirmation_login(user):
    confirmation_code = secrets.token_urlsafe(6)
    redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    redis_connection.set(f"confirmation_code:{user.id}", confirmation_code)

    user_created.delay(user.id, confirmation_code)


@csrf_exempt
def activate_logged_in_with_new_device(request, user_id, confirmation_code):
    user = get_object_or_404(User, id=user_id)

    redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    stored_code = redis_connection.get(f"confirmation_code:{user.id}")

    if stored_code.decode('utf-8') == confirmation_code:
        user.logged_in_with_new_device = True
        user.save()
        redis_connection.delete(f"confirmation_code:{user.id}")
        return JsonResponse({'message': 'Аккаунт успешно активирован.'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Неверный код подтверждения.'}, status=status.HTTP_401_UNAUTHORIZED)
    

# смена пароля и смена эл.почты в профиле
def generate_code(length):
    code = ''.join(random.choices(string.digits, k=length))
    return code

@csrf_exempt
def email_change_code_func(request, email):
    confirmation_code = generate_code(4)
    redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    redis_connection.set(f"confirmation_code:{email}", confirmation_code)

    email_change_code.delay(email, confirmation_code)

    return JsonResponse({'message': 'Код отправился'}, status=status.HTTP_200_OK)
    

@csrf_exempt
def change_email_func(request, email, new_email, confirmation_code):
    user = get_object_or_404(User, email=email)

    redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    stored_code = redis_connection.get(f"confirmation_code:{email}")

    if stored_code.decode('utf-8') == confirmation_code:
        user.email = new_email
        user.save()
        redis_connection.delete(f"confirmation_code:{email}")
        return JsonResponse({'message': 'Эл. почта изменена'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Неверный код подтверждения.'}, status=status.HTTP_401_UNAUTHORIZED)

# смена пароля
@csrf_exempt
def password_change_code_func(request, email):
    confirmation_code = generate_code(4)
    redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    redis_connection.set(f"confirmation_code_password:{email}", confirmation_code)

    password_change_code.delay(email, confirmation_code)
    # result = password_change_code.delay(email, confirmation_code)

    return JsonResponse({'message': 'код отправлен'}, status=status.HTTP_200_OK)
    
    # return HttpResponse("Password change code sent successfully.")


@csrf_exempt
def confirm_code_change_password(request, email, new_password, confirmation_code):
    user = get_object_or_404(User, email=email)

    redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    stored_code = redis_connection.get(f"confirmation_code_password:{email}")

    if stored_code.decode('utf-8') == confirmation_code:
        user.password = make_password(new_password)
        user.save()
        redis_connection.delete(f"confirmation_code_password:{email}")
        return JsonResponse({'message': 'Пароля успешно изменен.'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Ошибка при смене пароля.'}, status=status.HTTP_401_UNAUTHORIZED)
    