from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, request, Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, FormView
from django.db.models import Max, Min, Avg, Sum, Count
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers, status, mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from carousel.models import CarouselModel
from cart.forms import CartAddProductForm
from help.models import HelpModel
from products import models, forms
from products.forms import ReviewForm
from products.models import ProductModel, ProductAttributes, ReviewModel, CategoryModel, ProductImageModel, \
    ReviewImageModel
from cart.cart import Cart
from products.serializers import ProductSerializer, ProductRatingSerializer, CarouselSerializer, HelpSerializer, \
    CategorySerializer, ProductDetailSerializer, ProductImageModelSerializer, ProductDiscountSerializer, \
    ReviewModelSerializer, ReviewCreateSerializer
from products.utils import get_wishlist_data, get_cart_data


class HomeTemplate(TemplateView):
    template_name = 'index.html'

    def get_object(self, queryset=None):
        obj, created = self.model.objects.get_or_create(bar='foo bar baz')
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()

        return context


class ProductTemplate(ListView):
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_object(self, queryset=None):
        obj, created = self.model.objects.get_or_create(bar='foo bar baz')
        return obj

    def get_queryset(self, ):
        q = self.request.GET.get('q', '')
        price = self.request.GET.get('price')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')

        filters = {}

        if q:
            filters['title__icontains'] = q

        if category:
            filters['category_id'] = category

        if subcategory:
            filters['subcategory_id'] = subcategory

        if price:
            price_from, price_to = price.split(';')
            filters['price__gte'] = price_from
            filters['price__lte'] = price_to

        return ProductModel.objects.filter(**filters).order_by('pk')[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['cart'] = Cart(self.request)
        context['total_data'] = ProductModel.objects.count()
        context['min_price'], context['max_price'] = ProductModel.objects.aggregate(
            Min('real_price'),
            Max('real_price')
        ).values()

        return context


class ProductDetailView(DetailView):
    template_name = 'shop/product/detail.html'
    model = ProductModel
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['related'] = ProductModel.objects.order_by('-pk')
        context['colors'] = ProductAttributes.objects.all().values('color__id', 'color__code').distinct()
        return context

    def add_to_object(request, pk):
        try:
            object = ProductModel.objects.get(pk=pk)
        except ProductModel.DoesNotExist:
            return Response(data={'status': False})
        cart = request.session.get('cart', [])
        if object.pk in cart:
            cart.remove(object.pk)
            data = {'status': True, 'added': False}
        else:
            cart.append(object.pk)
            data = {'status': True, 'added': True}
        request.session['cart'] = cart

        data['cart_len'] = get_cart_data(cart)
        return JsonResponse(data)


class ProductDeleteView(DeleteView):
    model = ProductModel
    success_url = "/"
    template_name = "basket.html"


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST, request.FILES)
        product = ProductModel.objects.get(id=request[pk])
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


def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = ProductModel.objects.all().order_by('id')[offset:offset + limit]
    t = render_to_string('layouts/product-block.html', {'data': data})
    return JsonResponse({'data': t})


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


@login_required
def create_carts(request, pk):
    # product = get_object_or_404(ProductModel, pk=pk)
    # cart = request.session.get('cart', [])
    #
    # if request.user in product.cart.all():
    #     product.cart.remove(request.user)
    # else:
    #     product.cart.add(request.user)
    #
    # product.save()
    #
    # return redirect('order')
    pass


class AboutTemplateView(TemplateView):
    template_name = 'about.html'


class ContactTemplateView(TemplateView):
    template_name = 'contacts.html'


class OrderTemplateView(ListView):
    template_name = 'order.html'

    def get_queryset(self):
        return ProductModel.get_from_cart(self.request)


class ArticleTemplateView(TemplateView):
    template_name = 'articles.html'


# API

class ProductRatingAPIView(APIView):
    ''' Рейтинг продуктов '''

    def get(self, request):
        ratings = ReviewModel.objects.all()
        serializer = ProductRatingSerializer(ratings, many=True)
        return Response(serializer.data)


class ProductDiscountAPIView(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductDiscountSerializer


class ProductListAPIView(generics.ListAPIView):
    ''' Все продукты '''
    queryset = ProductModel.objects.filter().order_by('pk')
    serializer_class = ProductSerializer

    def get_extra_counts(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.aggregate(
            Min('real_price'),
            Max('real_price')
        )


class ProductImageModelAPIView(generics.ListAPIView):
    queryset = ProductImageModel.objects.all()
    serializer_class = ProductImageModelSerializer


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        products = ProductModel.objects.get(id=pk)
        serializer = ProductDetailSerializer(products, context={'request': request})
        return Response(serializer.data)


class CarouselListAPIView(generics.ListAPIView):
    ''' Карусель '''
    queryset = CarouselModel.objects.all()
    serializer_class = CarouselSerializer
    # def get(self, request),
    #     carousels = CarouselModel.objects.all()
    #     serializer = CarouselSerializer(carousels, many=True)
    #     return Response(serializer.data)


class HelpListAPIView(generics.ListAPIView):
    ''' Помощь '''
    queryset = HelpModel.objects.all()
    serializer_class = HelpSerializer


class CategoryListAPIView(generics.ListAPIView):
    ''' Категории '''
    queryset = CategoryModel.objects.filter(parent=None)
    serializer_class = CategorySerializer


class CountryListAPIView(APIView):
    def get(self, request):
        return Response([
            {
                "name": "Москва"
            },
            {
                "name": "Санкт-Петербург "
            },
            {
                "name": "Новосибирск, Новосибирская область"
            },
            {
                "name": "Екатеринбург, Свердловская область"
            },
            {
                "name": "Нижний Новгород, Нижегородская область"
            },
            {
                "name": "Казань"
            },
            {
                "name": "Самара"
            },
            {
                "name": "Челябинск"
            },
            {
                "name": "Омск, Омская область"
            },
            {
                "name": "Ростов-на-дону, Ростовская область"
            },
            {
                "name": "Уфа, Республика Башкортостан"
            },
            {
                "name": "Красноярск, Красноярский край"
            },
            {
                "name": "Пермь, Пермский край"
            },
            {
                "name": "Волгоград, Волгоградская область"
            },
            {
                "name": "Воронеж, Воронежская область"
            },
            {
                "name": "Саратов, Саратовская область"
            },
            {
                "name": "Краснодар, Краснодарский край"
            },
            {
                "name": "Тольятти, Самарская область"
            },
            {
                "name": "Тюмень, Тюменская область"
            },
            {
                "name": "Ижевск, Республика Удмуртия"
            },
            {
                "name": "Барнаул, Алтайский край"
            },
            {
                "name": "Ульяновск, Ульяновская область"
            },
            {
                "name": "Иркутск, Иркутская область"
            },
            {
                "name": "Владивосток, Приморский край"
            },
            {
                "name": "Ярославль, Ярославская область"
            },
            {
                "name": "Хабаровск, Хабаровский край"
            },
            {
                "name": "Махачкала, Республика Дагестан"
            },
            {
                "name": "Оренбург, Оренбургская область"
            },
            {
                "name": "Томск, Томская область"
            },
            {
                "name": "Новокузнецк, Кемеровская область"
            },
            {
                "name": "Кемерово, Кемеровская область"
            },
            {
                "name": "Астрахань, Астраханская область"
            },
            {
                "name": "Рязань, Рязанская область"
            },
            {
                "name": "Набережные челны"
            },
            {
                "name": "Пенза, Пензенская область"
            },
            {
                "name": "Липецк, Липецкая область"
            },
            {
                "name": "Тула, Тульская область"
            },
            {
                "name": "Киров, Кировская область"
            },
            {
                "name": "Чебоксары, Республика Чувашия"
            },
            {
                "name": "Калининград, Калининградская область"
            },
            {
                "name": "Курск, Курская область"
            },
            {
                "name": "Улан-Удэ, Республика Бурятия"
            },
            {
                "name": "Ставрополь, Ставропольский край"
            },
            {
                "name": "Магнитогорск"
            },
            {
                "name": "Тверь, Тверская Область"
            },
            {
                "name": "Иваново, Ивановская область"
            },
            {
                "name": "Брянск, Брянская область"
            },
            {
                "name": "Сочи, Краснодарский край"
            },
            {
                "name": "Белгород, Белгородская область"
            },
            {
                "name": "Сургут, Ханты-Мансийский АО. г. Сургут"
            }
        ])


# class ReviewAddCreateAPIView(APIView):
#     def post(self, request):
#         serializers = ReviewCreateSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response({'post': serializers.data})


class ReviewModelSerializerListAPIView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request, pk):
        reviews = ReviewModel.objects.filter(product=pk)
        serializer = ReviewModelSerializer(reviews, context={'request': request}, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return ReviewModel.objects.get(pk=pk)
        except ReviewModel.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        # snippet = self.get_object(pk)
        # serializer = ReviewModelSerializer(snippet, data=request.data)
        # if serializer.is_valid():
        rev = request.data.get('review_id', 0)
        reviews = ReviewModel.objects.get(pk=rev)
        reviews.review_count += 1
        reviews.save()
        # serializer.save()
        return Response(status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # return Response({"pk":pk})


class AddRatingViewSet(APIView):
    serializer_class = ReviewCreateSerializer
    parser_classes = [MultiPartParser]

    def get_object(self, pk=None):
        if pk:
            pass
        reviews = ReviewModel.objects.all()
        return reviews

    def get(self, request, **kwargs):
        if 'pk' in kwargs:
            pass
        sort_type = request.data.get('sort_type', '-created_at')
        reviews = self.get_object().order_by(sort_type)
        serializer = self.serializer_class(reviews, context={'request': request},  many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # serializer = self.serializer_class(data=request.data)
        # print(request.FILES.getlist('images'))
        product = ProductModel.objects.get(id=int(request.data['product']))
        # address = MapModel.objects.get(id=int(request.data['address']))
        reviews = ReviewModel.objects.create(
            name=request.data['name'],
            email=request.data['email'],
            rating=request.data['rating'],
            comments=request.data['comments'],
            product=product,
        )
        image = request.FILES.getlist('images')
        # print(image)
        for img_name in image:
            img = ReviewImageModel.objects.create(image=img_name)
            reviews.images.add(img)
            # print(img)
            reviews.save()

        return Response(self.serializer_class(reviews, context={'request': request}).data,  status=status.HTTP_201_CREATED)


