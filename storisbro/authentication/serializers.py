import secrets

import redis
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .tasks import user_created, user_login_code
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()

        # Генерация и сохранение кода в Redis
        confirmation_code = secrets.token_urlsafe(6)
        redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        redis_connection.set(f"confirmation_code:{user.id}", confirmation_code)

        # Запуск задачи по отправке письма
        user_created.delay(user.id, confirmation_code)

        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['id'] = self.user.id  # Добавляем ID пользователя

        if not self.user.is_active:
            raise serializers.ValidationError("Аккаунт не активирован.")
        
        confirmation_code = secrets.token_urlsafe(6)
        redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        redis_connection.set(f"confirmation_code:{self.user.id}", confirmation_code)

        # Запуск задачи по отправке письма
        user_login_code.delay(self.user.id, confirmation_code)

        return data

    class Meta:
        model = User
        fields = ('id', 'email', 'password')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        # fields = '__all__'