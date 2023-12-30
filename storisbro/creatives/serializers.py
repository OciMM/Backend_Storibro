from rest_framework import serializers

from .models import AddSingleCreative, AddDoubleCreative, RepostCreative, StickerCreative, DoubleStickerCreative

class AddSingleCreativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddSingleCreative
        fields = '__all__'


class AddDoubleCreativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddDoubleCreative
        fields = '__all__'


class RepostCreativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepostCreative
        fields = '__all__'


class StickerCreativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StickerCreative
        fields = '__all__'


class DoubleStickerCreativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoubleStickerCreative
        fields = '__all__'