from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import CommunityModel, Setting, CommunitySetting
from .serializers import CommunityModelSerializer, CommunitySettingSerializer
from .services import add_new_community_of_link

class CommunityModelAPIView(APIView):
    def get(self, request):
        try:
            community_model = CommunityModel.objects.all()
            serializer = CommunityModelSerializer(community_model, many=True)
            return Response(serializer.data)
        except CommunityModel.DoesNotExist:
            return Response(status=404)
        
    def post(self, request):
        url = request.data.get('url')
        if not url:
            return Response({'error': 'Отсутствует URL'}, status=status.HTTP_400_BAD_REQUEST)
        
        community_data = add_new_community_of_link(url)
        if community_data:
            name = community_data['name']
            photo = community_data['photo']

            community = CommunityModel.objects.create(name=name, photo=photo, url=url)
            serializer = CommunityModelSerializer(community)

            setting = Setting.objects.first()

            # Если объектов нет, можно обработать эту ситуацию
            if not setting:
                return Response({'error': 'Нет доступных статусов'}, status=status.HTTP_400_BAD_REQUEST)

            # Создание объекта CommunitySetting и связь с CommunityModel и Setting
            CommunitySetting.objects.create(community=community, status=setting)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'Группа не удовлетворяет условиям'}, status=status.HTTP_400_BAD_REQUEST)


class CommunitySettingAPIView(APIView):
    def get(self, request):
        setting_model = CommunitySetting.objects.all()
        serializer = CommunitySettingSerializer(setting_model, many=True)
        return Response(serializer.data)
    

class UpdateCommunitySettingAPIView(APIView):
    def get(self, request, pk):
        try:
            setting_model = CommunitySetting.objects.get(pk=pk)
            serializer = CommunitySettingSerializer(setting_model)
            return Response(serializer.data)
        except CommunitySetting.DoesNotExist:
            return Response(status=404)
        
    def patch(self, request, pk):
        try:
            setting_model = CommunitySetting.objects.get(pk=pk)
            serializer = CommunitySettingSerializer(setting_model, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except CommunitySetting.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)