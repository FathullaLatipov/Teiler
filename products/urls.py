from django.urls import path, include

from products.views import ProductTemplate, ProductDetailView

app_name = 'product'

urlpatterns = [
    path('', ProductTemplate.as_view(), name='products'),
    path('<int:pk>/', ProductDetailView.as_view(), name='single')
]