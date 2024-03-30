from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Statistics
from .serializers import StatisticSerializer
from .services import registered_users_count


class StatisticsAPIView(APIView):
    def get(self, request, start_date, end_date):
        if not start_date or not end_date:
            return Response({"error": "Необходимо указать start_date и end_date в параметрах запроса."}, status=status.HTTP_400_BAD_REQUEST)

        # Вызовите вашу функцию из services.py, передав параметры start_date и end_date
        registered_users_count(start_date, end_date)

        # Получите объект статистики после обновления ваших данных
        statistics = Statistics.objects.first()

        # Верните нужные поля статистики в ответе
        response_data = {
            'registered_users': statistics.registered_users,
            'registered_users_owner': statistics.registered_users_owner,
            'registered_users_client': statistics.registered_users_client,
            'creative_uploads': statistics.creative_uploads,
            'community_uploads': statistics.community_uploads,
            'story_views': statistics.story_views,  # Подставьте поле, если используете в вашей модели
            # Добавьте другие поля по необходимости
        }

        # Верните ответ с данными статистики и статусом 200
        return Response(response_data, status=status.HTTP_200_OK)