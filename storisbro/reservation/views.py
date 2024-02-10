from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import DateOfReservation
from .serializers import DateOfReservationSerializer

    
class DateOfReservationAPIView(APIView):
    def get(self, request):
        reservation_model = DateOfReservation.objects.all()
        serializer = DateOfReservationSerializer(reservation_model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DateOfReservationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)