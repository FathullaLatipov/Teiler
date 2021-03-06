from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.db.models import Max, Min, Q
from django.http import JsonResponse
from rest_framework.response import Response
from products.forms import ReviewForm
from products.models import ProductModel
from products.utils import get_wishlist_data, get_cart_data


class HomeTemplate(TemplateView):
    template_name = 'index.html'


class ProductTemplate(ListView):
    template_name = 'products.html'
    context_object_name = 'products'

    def get_object(self, queryset=None):
        obj, created = self.model.objects.get_or_create(bar='foo bar baz')
        return obj

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        price = self.request.GET.get('price')
        filters = {}

        if q:
            filters['title__contains'] = q

        if price:
            price_from, price_to = price.split(';')
            filters['price__gte'] = price_from
            filters['price__lte'] = price_to

        return ProductModel.objects.filter(**filters).order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['min_price'], context['max_price'] = ProductModel.objects.aggregate(
            Min('real_price'),
            Max('real_price')
        ).values()

        return context


class ProductDetailView(DetailView):
    template_name = 'single-product.html'
    model = ProductModel
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related'] = ProductModel.objects.order_by('-pk')
        return context


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST, request.FILES)
        product = ProductModel.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.image = request.FILES['image']
            form.save()
            print(request.POST)
        return redirect("/")


# def add_review(request, pk):
#     if request.method == 'POST':
#         product = ProductModel.objects.get(pk=pk)
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             form.save(commit=False)
#             form.product = product
#             form.save()
#     return redirect('/')


class WishlistModelListView(ListView):
    template_name = 'favs.html'
    paginate_by = 7

    def get_queryset(self):
        return ProductModel.get_from_wishlist(self.request)


def add_to_wishlist(request, pk):
    try:
        product = ProductModel.objects.get(pk=pk)
    except ProductModel.DoesNotExist:
        return Response(data={'status': False})
    wishlist = request.session.get('wishlist', [])
    if product.pk in wishlist:
        wishlist.remove(product.pk)
        data = {'status': True, 'added': False}
    else:
        wishlist.append(product.pk)
        data = {'status': True, 'added': True}
    request.session['wishlist'] = wishlist

    data['wishlist_len'] = get_wishlist_data(wishlist)
    return JsonResponse(data)


class CartModelListView(ListView):
    template_name = 'basket.html'
    paginate_by = 7

    def get_queryset(self):
        return ProductModel.get_from_cart(self.request)


def add_to_cart(request, pk):
    try:
        product = ProductModel.objects.get(pk=pk)
    except ProductModel.DoesNotExist:
        return Response(data={'status': False})
    cart = request.session.get('cart', [])
    if product.pk in cart:
        cart.remove(product.pk)
        data = {'status': True, 'added': False}
    else:
        cart.append(product.pk)
        data = {'status': True, 'added': True}
    request.session['cart'] = cart

    data['cart_len'] = get_cart_data(cart)
    return JsonResponse(data)


class AboutTemplateView(TemplateView):
    template_name = 'about.html'


class ArticleTemplateView(TemplateView):
    template_name = 'articles.html'

