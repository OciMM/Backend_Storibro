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
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='users')
    user_permissions = models.ManyToManyField(Permission, related_name='users')
    logged_in_with_new_device = models.BooleanField(default=False)
    status_commission = models.BooleanField(default=False, verbose_name="Статус пониженной комиссии")

    objects = UserManager()

    USERNAME_FIELD = 'email' 