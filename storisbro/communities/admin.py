from django.contrib import admin
from .models import StatusCommunities, CommunityModel, Setting, CommunitySetting

admin.site.register(StatusCommunities)
admin.site.register(CommunityModel)
admin.site.register(Setting)
admin.site.register(CommunitySetting)
