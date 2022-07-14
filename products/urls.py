from django.urls import path

from products.views import ProductTemplate

urlpatterns = [
    path('', ProductTemplate.as_view())
]