from django.urls import path, include

from products.views import ProductTemplate, ProductDetailView, AddReview, WishlistModelListView, add_to_wishlist

from . import views

app_name = 'product'

urlpatterns = [
    path('', ProductTemplate.as_view(), name='products'),
    path('<int:pk>/', ProductDetailView.as_view(), name='single'),
    path('products/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('wishlist/', WishlistModelListView.as_view(), name='wishlist'),
    path('wishlist/<int:pk>/', add_to_wishlist, name='add-wishlist'),
]