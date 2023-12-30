from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import AddSingleCreative, AddDoubleCreative, RepostCreative, StickerCreative, DoubleStickerCreative
from .serializers import AddSingleCreativeSerializer, AddDoubleCreativeSerializer, \
    RepostCreativeSerializer, StickerCreativeSerializer, DoubleStickerCreativeSerializer

from .service import check_link_for_story, check_size_file, check_is_story

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

        serializer = AddSingleCreativeSerializer(data=other_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    