# src/api/serializers/classification_serializer.py
from rest_framework import serializers
from ..models.classification_model import Classification

class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = '__all__'
