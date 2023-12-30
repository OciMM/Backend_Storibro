from django.contrib import admin
from .models import UserModel, PublicModel

admin.site.register(UserModel)
admin.site.register(PublicModel)
