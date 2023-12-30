from django.contrib import admin
from .models import CommunityModel, Setting, CommunitySetting

admin.site.register(CommunityModel)
admin.site.register(Setting)
admin.site.register(CommunitySetting)
