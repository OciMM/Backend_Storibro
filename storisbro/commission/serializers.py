from rest_framework import serializers
from .models import UserModel, PublicModel


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class PublicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicModel
        fields = '__all__'
