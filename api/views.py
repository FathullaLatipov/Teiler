from django.shortcuts import render
from rest_framework import generics

from .models import TestModel
from . import serializers


class TestList(generics.ListAPIView):
    queryset = TestModel.objects.all()
    serializer_class = serializers.TestSerializer
