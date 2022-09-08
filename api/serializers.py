from rest_framework import serializers

from .models import TestModel


class TestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=300)
    description = serializers.models.TextField()

    class Meta:
        model = TestModel
        fields = ['title', 'pk', 'description', 'created_at']
