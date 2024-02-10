from rest_framework import serializers
from .models import DateOfReservation


class DateOfReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateOfReservation
        fields = '__all__'