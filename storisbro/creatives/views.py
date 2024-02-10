from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import AddSingleCreative, AddDoubleCreative, RepostCreative, StickerCreative, DoubleStickerCreative
from .serializers import AddSingleCreativeSerializer, AddDoubleCreativeSerializer, \
    RepostCreativeSerializer, StickerCreativeSerializer, DoubleStickerCreativeSerializer
from reservation.models import DateOfReservation

from .service import check_link_for_story, check_size_file, check_is_story
from django.db import transaction
import logging

# Настройка логгера
logging.basicConfig(level=logging.DEBUG)  # Установите уровень логгирования по вашему усмотрению

# Получение логгера для текущего модуля
logger = logging.getLogger(__name__)

class AddSingleCreativeAPIView(APIView):
    """Одиночный креатив и его проверка"""
    
    def get(self, request):
        creative_model = AddSingleCreative.objects.all()
        serializer = AddSingleCreativeSerializer(creative_model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        link = request.data.get('link')
        if not link:
            return Response({'error': 'Отсутствует URL'}, status=status.HTTP_400_BAD_REQUEST)

        checked_link = check_link_for_story(link)
        if not checked_link:
            return Response({'error': 'Некорректная или нерабочая ссылка'}, status=status.HTTP_400_BAD_REQUEST)

        # Получите все данные из запроса, за исключением 'link'
        other_data = request.data.copy()
        del other_data['link']

        # Дополните данные 'link' после проверки
        other_data['link'] = checked_link
        print(other_data['file'])
        serializer = AddSingleCreativeSerializer(data=other_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        try:
            creative_model = AddSingleCreative.objects.get(pk=pk)
            serializer = AddSingleCreativeSerializer(creative_model, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AddSingleCreative.DoesNotExist:
            return Response(status=404)


class PK_AddSingleCreativeAPIView(APIView):
    """Проверка определенного одиночного креатива"""
    def get(self, request, pk):
        try:
            creative_model = AddSingleCreative.objects.get(pk=pk)
            serializer = AddSingleCreativeSerializer(creative_model)
            return Response(serializer.data)
        except AddSingleCreative.DoesNotExist:
            return Response(status=404)

    def patch(self, request, pk):
        try:
            creatives_model = AddSingleCreative.objects.get(pk=pk)
            serializer = AddSingleCreativeSerializer(creatives_model, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.data)
        except AddSingleCreative.DoesNotExist:
            return Response(status=404)


class AddDoubleCreativeAPIView(APIView):
    """Двойные креативы и их проверка"""
    def get(self, request):
        creative_model = AddDoubleCreative.objects.all()
        serializer = AddDoubleCreativeSerializer(creative_model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        first_link = request.data.get('first_link')
        second_link = request.data.get('second_link')
        if not first_link and not second_link:
            return Response({'error': 'Отсутствует URL одной из ссылок'}, status=status.HTTP_400_BAD_REQUEST)

        checked_link_first = check_link_for_story(first_link)
        checked_link_second = check_link_for_story(second_link)

        if not checked_link_first and not checked_link_second:
            return Response({'error': 'Некорректная или нерабочая одна из ссылок'}, status=status.HTTP_400_BAD_REQUEST)

        # Получите все данные из запроса, за исключением 'link'
        other_data = request.data.copy()
        del other_data['first_link']
        del other_data['second_link']

        # Дополните данные 'link' после проверки
        other_data['first_link'] = checked_link_first
        other_data['second_link'] = checked_link_second

        serializer = AddDoubleCreativeSerializer(data=other_data)
        if serializer.is_valid():

            file = request.data.get('file')

            # Проверка размера файла
            if not check_size_file(file.temporary_file_path()):
                return Response({"error": "Размер файла слишком большой."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PK_AddDoubleCreativeAPIView(APIView):
    """Проверка определенного двойного креатива"""
    def get(self, request, pk):
        try:
            creative_model = AddDoubleCreative.objects.get(pk=pk)
            serializer = AddDoubleCreativeSerializer(creative_model)
            return Response(serializer.data)
        except AddDoubleCreative.DoesNotExist:
            return Response(status=404)
        
    def patch(self, request, pk):
        try:
            creatives_model = AddDoubleCreative.objects.get(pk=pk)
            serializer = AddDoubleCreativeSerializer(creatives_model, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.data)
        except AddDoubleCreative.DoesNotExist:
            return Response(status=404)


class RepostCreativeAPIView(APIView):
    """Репосты и их проверка"""
    def get(self, request):
        repost_model = RepostCreative.objects.all()
        serializer = RepostCreativeSerializer(repost_model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        link_of_story = request.data.get('link_of_story')
        
        if not link_of_story:
            return Response({'error': 'Отсутствует URL'}, status=status.HTTP_400_BAD_REQUEST)
        
        checked_link = check_is_story(link_of_story)
        if not checked_link:
            return Response({'error': 'Некорректная или нерабочая ссылка'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RepostCreativeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PK_RepostCreativeAPIView(APIView):
    """Проверка определенного репоста"""
    def get(self, request, pk):
        try:
            creative_model = RepostCreative.objects.get(pk=pk)
            serializer = RepostCreativeSerializer(creative_model)
            return Response(serializer.data)
        except RepostCreative.DoesNotExist:
            return Response(status=404)
        
    def patch(self, request, pk):
        try:
            creatives_model = RepostCreative.objects.get(pk=pk)
            serializer = RepostCreativeSerializer(creatives_model, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.data)
        except RepostCreative.DoesNotExist:
            return Response(status=404)


class StickerCreativeAPIView(APIView):
    """Ссылки-стикеры и их проверка"""
    def get(self, request):
        repost_model = StickerCreative.objects.all()
        serializer = StickerCreativeSerializer(repost_model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        link_of_story = request.data.get('link_of_story')
        
        if not link_of_story:
            return Response({'error': 'Отсутствует URL'}, status=status.HTTP_400_BAD_REQUEST)
        
        checked_link = check_is_story(link_of_story)
        if not checked_link:
            return Response({'error': 'Некорректная или нерабочая ссылка'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StickerCreativeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PK_StickerCreativeAPIView(APIView):
    """Проверка определенной ссылки-стикера"""
    def get(self, request, pk):
        try:
            creative_model = StickerCreative.objects.get(pk=pk)
            serializer = StickerCreativeSerializer(creative_model)
            return Response(serializer.data)
        except StickerCreative.DoesNotExist:
            return Response(status=404)
        
    def patch(self, request, pk):
        try:
            creatives_model = StickerCreative.objects.get(pk=pk)
            serializer = StickerCreativeSerializer(creatives_model, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.data)
        except StickerCreative.DoesNotExist:
            return Response(status=404)


class DoubleStickerCreativeAPIView(APIView):
    """Двойные ссылки-стикеры и их проверка"""
    def get(self, request):
        sticker_model = DoubleStickerCreative.objects.all()
        serializer = DoubleStickerCreativeSerializer(sticker_model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        link_of_story_first = request.data.get('link_of_story_first')
        link_of_story_second = request.data.get('link_of_story_second')
        
        if not link_of_story_first and not link_of_story_second:
            return Response({'error': 'Отсутствует URL'}, status=status.HTTP_400_BAD_REQUEST)
        
        checked_link_first = check_is_story(link_of_story_first)
        checked_link_second = check_is_story(link_of_story_second)

        if not checked_link_first and not checked_link_second:
            return Response({'error': 'Некорректная или нерабочая ссылка'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DoubleStickerCreativeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PK_DoubleStickerCreativeAPIView(APIView):
    """Проверка определенной двойной ссылки-стикера"""
    def get(self, request, pk):
        try:
            creative_model = DoubleStickerCreative.objects.get(pk=pk)
            serializer = DoubleStickerCreativeSerializer(creative_model)
            return Response(serializer.data)
        except DoubleStickerCreative.DoesNotExist:
            return Response(status=404)
    
    def patch(self, request, pk):
        try:
            creatives_model = DoubleStickerCreative.objects.get(pk=pk)
            serializer = DoubleStickerCreativeSerializer(creatives_model, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.data)
        except DoubleStickerCreative.DoesNotExist:
            return Response(status=404)


class AllCreativesAPIView(APIView):
    """Эндпоинт для объединения данных из разных сериализаторов"""

    def get(self, request):
        single_creative_model = AddSingleCreative.objects.all()
        single_creative_serializer = AddSingleCreativeSerializer(single_creative_model, many=True).data

        double_creative_model = AddDoubleCreative.objects.all()
        double_creative_serializer = AddDoubleCreativeSerializer(double_creative_model, many=True).data

        repost_model = RepostCreative.objects.all()
        repost_serializer = RepostCreativeSerializer(repost_model, many=True).data

        sticker_model = StickerCreative.objects.all()
        sticker_serializer = StickerCreativeSerializer(sticker_model, many=True).data

        double_sticker_model = DoubleStickerCreative.objects.all()
        double_sticker_serializer = DoubleStickerCreativeSerializer(double_sticker_model, many=True).data

        combined_data = []

        combined_data.extend(single_creative_serializer)
        combined_data.extend(double_creative_serializer)
        combined_data.extend(repost_serializer)
        combined_data.extend(sticker_serializer)
        combined_data.extend(double_sticker_serializer)

        return Response(combined_data)

    def patch(self, request):
        data = request.data
        saved_creatives = []
        errors = []
        logger.debug("Starting patch method...")
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    creative_type = item.get('creative_type')

                    if creative_type == 'AddSingleCreative':
                        try:
                            pk = item.get('id')
                            creative_model = AddSingleCreative.objects.get(pk=pk)
                            serializer = AddSingleCreativeSerializer(creative_model, data=item, partial=True)
                            
                            # Обработка ManyToManyField 'reservation'
                            reservation_data = item.get('reservation', [])
                            if reservation_data:
                                reservation_objects = []
                                for reservation_id in reservation_data:
                                    reservation_object = DateOfReservation.objects.get(id=id)
                                    reservation_objects.append(reservation_object)
                                serializer.validated_data['reservation'] = reservation_objects

                            if serializer.is_valid():
                                serializer.save()
                                saved_creatives.append(serializer.data)
                        except AddSingleCreative.DoesNotExist:
                            pass

                    elif creative_type == 'AddDoubleCreative':
                        try:
                            pk = item.get('id')
                            creative_model = AddDoubleCreative.objects.get(pk=pk)
                            serializer = AddDoubleCreativeSerializer(creative_model, data=item, partial=True)
                            if serializer.is_valid():
                                serializer.save()
                                saved_creatives.append(serializer.data)

                        except AddDoubleCreative.DoesNotExist:
                            pass

                    elif creative_type == 'RepostCreative':
                        try:
                            pk = item.get('id')
                            creative_model = RepostCreative.objects.get(pk=pk)
                            serializer = RepostCreativeSerializer(creative_model, data=item, partial=True)
                            if serializer.is_valid():
                                serializer.save()
                                saved_creatives.append(serializer.data)

                        except RepostCreative.DoesNotExist:
                            pass

                    elif creative_type == 'StickerCreative':
                        try:
                            pk = item.get('id')
                            creative_model = StickerCreative.objects.get(pk=pk)
                            serializer = StickerCreativeSerializer(creative_model, data=item, partial=True)
                            if serializer.is_valid():
                                serializer.save()
                                saved_creatives.append(serializer.data)

                        except StickerCreative.DoesNotExist:
                            pass

                    elif creative_type == 'DoubleStickerCreative':
                        try:
                            pk = item.get('id')
                            creative_model = DoubleStickerCreative.objects.get(pk=pk)
                            serializer = DoubleStickerCreativeSerializer(creative_model, data=item, partial=True)
                            if serializer.is_valid():
                                serializer.save()
                                saved_creatives.append(serializer.data)

                        except DoubleStickerCreative.DoesNotExist:
                            pass
        if errors:
            logger.error(f"Validation errors: {errors}")
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        
        logger.debug("Finishing patch method.")
        return Response({"message": "Креативы успешно обновлены", "saved_creatives": saved_creatives, "item": data})