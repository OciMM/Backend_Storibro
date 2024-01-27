"""
URL configuration for storisbro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from commission.views import PublicModelAPIView, UpdatePublicModelStatusAPIView, UserModelAPIView
from communities.views import CommunityModelAPIView, CommunitySettingAPIView, UpdateCommunitySettingAPIView, \
    PK_CommunityModelAPIView
from creatives.views import AddSingleCreativeAPIView, AddDoubleCreativeAPIView, RepostCreativeAPIView, \
    StickerCreativeAPIView, DoubleStickerCreativeAPIView, AllCreativesAPIView, PK_AddSingleCreativeAPIView, \
    PK_AddDoubleCreativeAPIView, PK_RepostCreativeAPIView, PK_StickerCreativeAPIView, PK_DoubleStickerCreativeAPIView
from reservation.views import CreativeModelAPIView, DateOfReservationAPIView, ImportPKCreativeModelAPIView
from user_test.views import UserAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('authentication.urls', 'authentication'), namespace='authentication')),
    path('confirmation/', include('confirmation.urls')),
    path('ref/', include('ref.urls')),

    path('notification/', include(('notification.urls', 'notification'), namespace='notification')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('user/<int:pk>', UserAPIView.as_view()),
    path('api_reservation/creatives', CreativeModelAPIView.as_view()),
    path('api_reservation/reservations', DateOfReservationAPIView.as_view()),
    path('api_reservation/creatives/<int:pk>', ImportPKCreativeModelAPIView.as_view()),
    
    path('api_creatives/add_single_creative', AddSingleCreativeAPIView.as_view()),
    path('api_creatives/add_single_creative/<int:pk>', PK_AddSingleCreativeAPIView.as_view()),

    path('api_creatives/add_double_creative', AddDoubleCreativeAPIView.as_view()),
    path('api_creatives/add_double_creative/<int:pk>', PK_AddDoubleCreativeAPIView.as_view()),

    path('api_creatives/add_repost_creative', RepostCreativeAPIView.as_view()),
    path('api_creatives/add_repost_creative/<int:pk>', PK_RepostCreativeAPIView.as_view()),

    path('api_creatives/add_sticker_creative', StickerCreativeAPIView.as_view()),
    path('api_creatives/add_sticker_creative/<int:pk>', PK_StickerCreativeAPIView.as_view()),

    path('api_creatives/add_double_sticker_creative', DoubleStickerCreativeAPIView.as_view()),
    path('api_creatives/add_double_sticker_creative/<int:pk>', PK_DoubleStickerCreativeAPIView.as_view()),

    path('api_creatives/all_creatives', AllCreativesAPIView.as_view()),
    path('api_communities/communities', CommunityModelAPIView.as_view()),
    path('api_communities/communities/<int:pk>', PK_CommunityModelAPIView.as_view()),
    path('api_communities/communities/community_setting', CommunitySettingAPIView.as_view()),
    path('api_communities/communities/community_setting/<int:pk>', UpdateCommunitySettingAPIView.as_view()),
    path('api_commission/publics', PublicModelAPIView.as_view()),
    path('api_commission/users', UserModelAPIView.as_view()),
    path('api_commission/publics/<int:pk>', UpdatePublicModelStatusAPIView.as_view())
]

