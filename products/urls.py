from django.urls import path, include

from products.views import ProductTemplate, ProductDetailView

from . import views

app_name = 'product'

urlpatterns = [
    path('', ProductTemplate.as_view(), name='products'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path('<int:pk>/', ProductDetailView.as_view(), name='single')
]