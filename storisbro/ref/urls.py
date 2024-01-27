from django.urls import path
from .views import referral_view, register_referral

urlpatterns = [
    path('referral/<int:referral_number>/', referral_view, name='referral_view'),
    path('register_referral/', register_referral, name='register_referral'),

]