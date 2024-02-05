from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from communities.models import CommunityModel
from communities.serializers import CommunityModelSerializer
from .services import check_link_in_community
from .tasks import run_patch_task_button
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404  # Добавлено для удобства
from django.http import JsonResponse
from rest_framework import status

from django.db.models.signals import post_save
from django.dispatch import receiver


# class PublicModelAPIView(ListAPIView):
#     queryset = CommunityModel.objects.all()
#     serializer_class = CommunityModelSerializer

class UpdatePublicModelStatusAPIView(APIView):
    def get(self, request, pk):
        try:
            public_model = CommunityModel.objects.get(pk=pk)
            serializer = CommunityModelSerializer(public_model)
            return Response(serializer.data)
        except CommunityModel.DoesNotExist:
            return Response(status=404)

    def patch(self, request, pk):
        try:
            public_model = CommunityModel.objects.get(pk=pk)
            link_found = check_link_in_community(public_model.url, public_model.url_commission)
            
            if link_found:
                public_model.status_commission = True
            else:
                public_model.status_commission = False

            public_model.save()
            serializer = CommunityModelSerializer(public_model)

            return Response(serializer.data)
        except CommunityModel.DoesNotExist:
            return Response(status=404)


@csrf_exempt
def low_commission(request, user_id):
    try:
        print(user_id)
        if run_patch_task_button.delay(user_id):
            return JsonResponse({'message': 'Проверка прошла!!!'})
        return JsonResponse({'message': 'Да я того все'})
    except Exception as e:
        print(f"Ошибка: {e}")
        return JsonResponse({'message': 'Проверка не прошла'})

# @receiver(post_save, sender=CommunityModel)
# def update_user_status(sender, instance, **kwargs):
#     user = instance.user
#     communities = CommunityModel.objects.filter(user=user)

#     all_community_true = all(community.status_commission for community in communities)

#     user.status_commission = all_community_true
#     user.save()
