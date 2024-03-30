from django.contrib import admin
from .models import TypeButton, AddSingleCreative, AddDoubleCreative, RepostCreative, StickerCreative, \
    DoubleStickerCreative, StatusCreative

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(TypeButton)
admin.site.register(StatusCreative, StatusAdmin)
admin.site.register(AddSingleCreative)
admin.site.register(AddDoubleCreative)
admin.site.register(RepostCreative)
admin.site.register(StickerCreative)
admin.site.register(DoubleStickerCreative)

