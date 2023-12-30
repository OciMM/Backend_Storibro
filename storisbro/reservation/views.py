from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CreativeModel, DateOfReservation
from .serializers import CreativeModelSerializer, DateOfReservationSerializer


class CreativeModelAPIView(APIView):
    def get(self, request):
        creative_model = CreativeModel.objects.all()
        serializer = CreativeModelSerializer(creative_model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CreativeModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Получаем данные из запроса
            date_id = request.data.get('date')  # Предполагается, что здесь будет указан ID DateOfReservation

            # Находим объект DateOfReservation по ID
            reservation_instance = DateOfReservation.objects.get(pk=date_id)

            # Проверяем, есть ли места для бронирования
            if reservation_instance.count_room > 0:
                # Уменьшаем количество мест на 1 и сохраняем изменения
                reservation_instance.count_room -= 1
                reservation_instance.save()

                # Сохраняем объект CreativeModel
                serializer.save()
                return Response(serializer.data)
            else:
                # Если нет мест, возвращаем ошибку
                return Response({"error": "Нет свободных мест для бронирования"}, status=status.HTTP_400_BAD_REQUEST)
    
class DateOfReservationAPIView(APIView):
    def get(self, request):
        reservation_model = DateOfReservation.objects.all()
        serializer = DateOfReservationSerializer(reservation_model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DateOfReservationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)