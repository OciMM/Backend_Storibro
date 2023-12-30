from rest_framework import serializers

from .models import CommunityModel, CommunitySetting


class CommunityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityModel
        fields = '__all__'


class CommunitySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunitySetting
        fields = '__all__'
