from django.contrib import admin
from .models import TypeButton, AddSingleCreative, AddDoubleCreative, RepostCreative, StickerCreative, \
    DoubleStickerCreative, StatusCreative

admin.site.register(TypeButton)
admin.site.register(StatusCreative)
admin.site.register(AddSingleCreative)
admin.site.register(AddDoubleCreative)
admin.site.register(RepostCreative)
admin.site.register(StickerCreative)
admin.site.register(DoubleStickerCreative)

