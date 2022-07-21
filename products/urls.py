from django.urls import path, include

from products.views import ProductTemplate, ProductDetailView, AddReview

from . import views

app_name = 'product'

urlpatterns = [
    path('', ProductTemplate.as_view(), name='products'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path('<int:pk>/', ProductDetailView.as_view(), name='single'),
    path('products/<int:pk>/', AddReview.as_view(), name='add_review'),
]