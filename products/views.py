from django.shortcuts import render
from django.views.generic import ListView

from products.models import ProductModel


class HomeTemplate(ListView):
    template_name = 'index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return ProductModel.objects.all()
