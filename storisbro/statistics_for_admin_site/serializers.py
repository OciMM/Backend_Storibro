from rest_framework import serializers
from .models import Statistics


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'
