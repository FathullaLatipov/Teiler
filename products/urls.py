from django.urls import path, include

from products.views import ProductTemplate, ProductDetailView, AddReview, WishlistModelListView, add_to_wishlist, \
    CartModelListView, add_to_cart

app_name = 'product'

urlpatterns = [
    path('', ProductTemplate.as_view(), name='products'),
    path('<int:pk>/', ProductDetailView.as_view(), name='single'),
    path('products/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('wishlist/', WishlistModelListView.as_view(), name='wishlist'),
    path('wishlist/<int:pk>/', add_to_wishlist, name='add-wishlist'),
    path('cart/', CartModelListView.as_view(), name='cart'),
    path('cart/<int:pk>/', add_to_cart, name='add-cart'),

]