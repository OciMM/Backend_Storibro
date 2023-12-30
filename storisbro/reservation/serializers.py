from rest_framework import serializers
from .models import CreativeModel, DateOfReservation

class CreativeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreativeModel
        fields = '__all__'

class DateOfReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateOfReservation
        fields = '__all__'