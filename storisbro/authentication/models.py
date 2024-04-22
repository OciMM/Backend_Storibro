from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # user.is_active = True  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='users')
    user_permissions = models.ManyToManyField(Permission, related_name='users')
    logged_in_with_new_device = models.BooleanField(default=False)
    name = models.CharField(max_length=100, verbose_name='Имя пользователя', blank=True, null=True)
    status_commission = models.BooleanField(default=False, verbose_name="Статус пониженной комиссии")
    status_owner = models.BooleanField(default=False, verbose_name='Статус владельца')
    statu_client = models.BooleanField(default=False, verbose_name='Статус заказчика')
    vk_id = models.CharField(max_length=200, verbose_name='VK id', blank=True, null=True)
    count_of_visit = models.PositiveIntegerField(default=0, verbose_name='Количество посещений на сайте')

    registration_date = models.DateTimeField(auto_now_add=True, null=True)
    replenishment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    withdrawal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    community_count = models.PositiveIntegerField(default=0)
    creative_count = models.PositiveIntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email' 