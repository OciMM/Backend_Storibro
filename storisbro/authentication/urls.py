from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import Home, UserCreateAPIView, activate_account, ObtainTokenView, UserProfileAPIView, activate_logged_in_with_new_device, \
    password_change_code_func, confirm_code_change_password, email_change_code_func

app_name = 'social'

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', ObtainTokenView.as_view(), name='token_obtain_pair'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('activate/<int:user_id>/<str:confirmation_code>/', activate_account, name='activate_account'),
    path('activate_login/<int:user_id>/<str:confirmation_code>/', activate_logged_in_with_new_device, name='activate_login'),
    path('password_change/<str:email>/', password_change_code_func),
    path('password_code_confirm/<str:email>/<str:confirmation_code>/', confirm_code_change_password),
    path('profile/', UserProfileAPIView.as_view()),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('home/', Home.as_view(), name='home'),

    path('change_email/<str:email>/', email_change_code_func),
]