from rest_framework import serializers

from .models import CommunityModel, CommunitySetting
from authentication.models import User


class CommunityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityModel
        fields = '__all__'


class CommunitySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunitySetting
        fields = '__all__'


# сериализатор для доступных сообществ
class CommunityAvailableForUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'vk_id')
