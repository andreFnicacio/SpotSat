# src/api/serializers/image_serializer.py
from rest_framework import serializers
from ..models.image_model import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
