from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from products.models import ProductModel


class HomeTemplate(TemplateView):
    template_name = 'index.html'


class ProductTemplate(ListView):
    template_name = 'products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return ProductModel.objects.all()


class ProductDetailView(DetailView):
    template_name = 'single-product.html'
    model = ProductModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related'] = ProductModel.objects.order_by('-pk')
        return context


class AboutTemplateView(TemplateView):
    template_name = 'about.html'


class ArticleTemplateView(TemplateView):
    template_name = 'articles.html'
