from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import PublicModel, UserModel
from .serializers import PublicModelSerializer, UserModelSerializer
from .services import check_link_in_community 

from django.db.models.signals import post_save
from django.dispatch import receiver

import schedule
import time
from random import randint
from datetime import datetime, timedelta

class UserModelAPIView(ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer

class PublicModelAPIView(ListAPIView):
    queryset = PublicModel.objects.all()
    serializer_class = PublicModelSerializer

class UpdatePublicModelStatusAPIView(APIView):
    def get(self, request, pk):
        try:
            public_model = PublicModel.objects.get(pk=pk)
            serializer = PublicModelSerializer(public_model)
            return Response(serializer.data)
        except PublicModel.DoesNotExist:
            return Response(status=404)

    def patch(self, request, pk):
        try:
            public_model = PublicModel.objects.get(pk=pk)
            link_to_check = public_model.url

            link_found = check_link_in_community(public_model.name, link_to_check)
            
            if link_found:
                public_model.status = True
            else:
                public_model.status = False

            public_model.save()
            serializer = PublicModelSerializer(public_model)

            # schedule_random_patch()

            return Response(serializer.data)
        except PublicModel.DoesNotExist:
            return Response(status=404)

@receiver(post_save, sender=PublicModel)
def update_user_status(sender, instance, **kwargs):
    user = instance.user
    communities = PublicModel.objects.filter(user=user)

    if instance.status is False:
        user.status = False
        user.save()
    else:
        all_community_true = any(community.status for community in communities)

        user.status = all_community_true
        user.save()
