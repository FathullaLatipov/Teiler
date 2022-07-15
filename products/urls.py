from django.urls import path

from products.views import ProductTemplate, ProductDetailView

app_name = 'product'

urlpatterns = [
    path('', ProductTemplate.as_view(), name='products'),
    # path('', ProductDetailView.as_view())
]