from django.urls import path

from products.views import ReviewModelSerializerListAPIView, AddRatingViewSet
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('api/v1/reviews/', ReviewModelSerializerListAPIView.as_view()),
    path('api/v1/add-review/', AddRatingViewSet.as_view()),
]