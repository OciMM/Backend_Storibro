from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from authentication.models import User

from .models import CommunityModel, Setting, CommunitySetting
from authentication.models import User
from .serializers import CommunityModelSerializer, CommunitySettingSerializer, CommunityAvailableForUser
from .services import add_new_community_of_link, add_new_community_of_name, list_of_available_communities, get_int_id

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
        name = request.data.get('name')
        
        if url:
        
            community_data = add_new_community_of_link(url)
            if community_data:
                name = community_data['name']
                # photo = community_data['photo']
                count_members = community_data['count_members']
                user_pk = request.data.get('user')
                
                try:
                    user = User.objects.get(pk=int(user_pk))
                except (User.DoesNotExist, ValueError):
                    return Response({'error': 'Некорректный пользователь'}, status=status.HTTP_400_BAD_REQUEST)
        
                community = CommunityModel.objects.create(user=user, name=name, count_members=count_members, url=url)
                serializer = CommunityModelSerializer(community)

                setting = Setting.objects.first()

                # Если объектов нет, можно обработать эту ситуацию
                if not setting:
                    return Response({'error': 'Нет доступных статусов'}, status=status.HTTP_400_BAD_REQUEST)

                # Создание объекта CommunitySetting и связь с CommunityModel и Setting
                CommunitySetting.objects.create(community=community, status=setting)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        elif name:
            community_data = add_new_community_of_name(name)
            if community_data:
                # photo = community_data['photo']
                count_members = community_data['count_members']
                url = community_data['url']
                user_pk = request.data.get('user')
                
                try:
                    user = User.objects.get(pk=int(user_pk))
                except (User.DoesNotExist, ValueError):
                    return Response({'error': 'Некорректный пользователь'}, status=status.HTTP_400_BAD_REQUEST)
        
                community = CommunityModel.objects.create(user=user, name=name, count_members=count_members, url=url)
                serializer = CommunityModelSerializer(community)

                setting = Setting.objects.first()

                # Если объектов нет, можно обработать эту ситуацию
                if not setting:
                    return Response({'error': 'Нет доступных статусов'}, status=status.HTTP_400_BAD_REQUEST)

                # Создание объекта CommunitySetting и связь с CommunityModel и Setting
                CommunitySetting.objects.create(community=community, status=setting)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'Группа не удовлетворяет условиям'}, status=status.HTTP_400_BAD_REQUEST)


class UserCommunityModelAPIView(APIView):
    def get(self, request, user):
        try:
            community_model = CommunityModel.objects.filter(user=user)
            serializer = CommunityModelSerializer(community_model, many=True)
            return Response(serializer.data)
        except CommunityModel.DoesNotExist:
            return Response(status=404)

# для настроек вывод инфы
class UserSettingCommunityModelAPIView(APIView):
    def get(self, request, user, pk):
        try:
            community_model = CommunityModel.objects.get(user=user, pk=pk)
            serializer = CommunityModelSerializer(community_model)
            return Response(serializer.data)
        except CommunityModel.DoesNotExist:
            return Response(status=404)
        
    def delete(self, request, user, pk):
        try:
            creative_model = CommunityModel.objects.get(user=user, pk=pk)
            creative_model.delete()
            return Response({"success": f"id {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)
        except creative_model.DoesNotExist:
            return Response({"error": f"with id {pk} not found"}, status=status.HTTP_404_NOT_FOUND)


class PK_CommunityModelAPIView(APIView):
    def get(self, request, pk):
        try:
            community_model = CommunityModel.objects.get(pk=pk)
            serializer = CommunityModelSerializer(community_model)
            return Response(serializer.data)
        except CommunityModel.DoesNotExist:
            return Response(status=404)
    
    def patch(self, request, pk):
        try:
            community_model = CommunityModel.objects.get(pk=pk)
            serializer = CommunityModelSerializer(community_model, data=request.data, partial=True)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.data)
        except CommunityModel.DoesNotExist:
            return Response(status=404)

# настройки сообществ
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
        

# Запрос на доступные к добавлению сообщества
class AvailableCommunitiesAPIView(APIView):
    def get(self, request, user_id):
        try:
            user_info = User.objects.get(pk=user_id)
            serializer = CommunityAvailableForUser(user_info)
            func_serializer = serializer.data

            user_int_id = get_int_id(func_serializer['vk_id'])

            info = list_of_available_communities(user_id=user_int_id)
            return Response({"list_publics": info[0], "list_avatars": info[1]})
        except User.DoesNotExist:
            return Response(status=404)


class AddAvailableCommunitiesAPIView(APIView):
    def post(self, request, arr_communities):
        url = request.data.get('url')
        name = request.data.get('name')
        
        if url:
        
            community_data = add_new_community_of_link(url)
            if community_data:
                name = community_data['name']
                # photo = community_data['photo']
                count_members = community_data['count_members']
                user_pk = request.data.get('user')
                
                try:
                    user = User.objects.get(pk=int(user_pk))
                except (User.DoesNotExist, ValueError):
                    return Response({'error': 'Некорректный пользователь'}, status=status.HTTP_400_BAD_REQUEST)
        
                community = CommunityModel.objects.create(user=user, name=name, count_members=count_members, url=url)
                serializer = CommunityModelSerializer(community)

                setting = Setting.objects.first()

                # Если объектов нет, можно обработать эту ситуацию
                if not setting:
                    return Response({'error': 'Нет доступных статусов'}, status=status.HTTP_400_BAD_REQUEST)

                # Создание объекта CommunitySetting и связь с CommunityModel и Setting
                CommunitySetting.objects.create(community=community, status=setting)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        elif name:
            community_data = add_new_community_of_name(name)
            if community_data:
                # photo = community_data['photo']
                count_members = community_data['count_members']
                url = community_data['url']
                user_pk = request.data.get('user')
                
                try:
                    user = User.objects.get(pk=int(user_pk))
                except (User.DoesNotExist, ValueError):
                    return Response({'error': 'Некорректный пользователь'}, status=status.HTTP_400_BAD_REQUEST)
        
                community = CommunityModel.objects.create(user=user, name=name, count_members=count_members, url=url)
                serializer = CommunityModelSerializer(community)

                setting = Setting.objects.first()

                # Если объектов нет, можно обработать эту ситуацию
                if not setting:
                    return Response({'error': 'Нет доступных статусов'}, status=status.HTTP_400_BAD_REQUEST)

                # Создание объекта CommunitySetting и связь с CommunityModel и Setting
                CommunitySetting.objects.create(community=community, status=setting)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'Группа не удовлетворяет условиям'}, status=status.HTTP_400_BAD_REQUEST)