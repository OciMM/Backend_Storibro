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
from django.conf import settings
from django.conf.urls.static import static

from commission.views import UpdatePublicModelStatusAPIView, low_commission
from communities.views import CommunityModelAPIView, CommunitySettingAPIView, UpdateCommunitySettingAPIView, \
    PK_CommunityModelAPIView, UserCommunityModelAPIView, UserSettingCommunityModelAPIView, AvailableCommunitiesAPIView
from creatives.views import AddSingleCreativeAPIView, AddDoubleCreativeAPIView, RepostCreativeAPIView, \
    StickerCreativeAPIView, DoubleStickerCreativeAPIView, AllCreativesAPIView, PK_AddSingleCreativeAPIView, \
    PK_AddDoubleCreativeAPIView, PK_RepostCreativeAPIView, PK_StickerCreativeAPIView, PK_DoubleStickerCreativeAPIView, \
    CreativeDetailAPIView, UserAllCreativesAPIView, UserAllCreativesDetailAPIView, UserCreativeDetailAPIView
from reservation.views import DateOfReservationAPIView
from authentication.views import UserAPIView, ChangeProfileData, AllEmailUsersAPIView
from statistics_for_admin_site.views import StatisticsAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('authentication.urls', 'authentication'), namespace='authentication')),
    path('api_users/users', UserAPIView.as_view()),
    path('api_users/change_profile/<int:pk>', ChangeProfileData.as_view()),
    path('api_users/check_email', AllEmailUsersAPIView.as_view()),
    path('confirmation/', include('confirmation.urls')),
    path('ref/', include('ref.urls')),

    path('notification/', include(('notification.urls', 'notification'), namespace='notification')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # path('api_reservation/creatives', CreativeModelAPIView.as_view()),
    path('api_reservation/reservations', DateOfReservationAPIView.as_view()),
    # path('api_reservation/creatives/<int:pk>', ImportPKCreativeModelAPIView.as_view()),
    
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

    path('api_creatives/all_creatives/<str:filter_date>', AllCreativesAPIView.as_view()),
    path('api_creatives/all_creatives/<str:creative_type>/<int:pk>/', CreativeDetailAPIView.as_view(), name='creative_detail'),
    path('api_creatives/own_all_creatives/<int:user>', UserAllCreativesAPIView.as_view()),
    path('api_creatives/own_detail_creatives/<int:user>/<int:pk>', UserAllCreativesDetailAPIView.as_view()),
    path('api_creatives/detail_user_creative/<int:user>/<str:creative_type>/<int:pk>', UserCreativeDetailAPIView.as_view()),    

    path('api/api_communities/communities', CommunityModelAPIView.as_view()),
    path('api_communities/available_publics/<int:user_id>', AvailableCommunitiesAPIView.as_view()),
    path('api_communities/own_communities/<int:user>', UserCommunityModelAPIView.as_view()),
    path('api_communities/settings_communities/<int:user>/<int:pk>', UserSettingCommunityModelAPIView.as_view()),
    path('api_communities/communities/<int:pk>', PK_CommunityModelAPIView.as_view()),
    path('api_communities/communities/community_setting', CommunitySettingAPIView.as_view()),
    path('api_communities/communities/community_setting/<int:pk>', UpdateCommunitySettingAPIView.as_view()),
    path('api_communities/communities/check_all/<int:user_id>', low_commission),
    path('api_communities/communities/check/<int:pk>', UpdatePublicModelStatusAPIView.as_view()),

    path('api_admin/statistics/<str:start_date>/<str:end_date>/', StatisticsAPIView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)