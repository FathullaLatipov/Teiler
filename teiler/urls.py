from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from cart import views
from help.views import HelpListView
from products.views import HomeTemplate, AboutTemplateView, ContactTemplateView, OrderTemplateView, load_more_data, \
    ProductListAPIView, ProductRatingAPIView, CarouselListAPIView, HelpListAPIView, CategoryListAPIView, \
    ProductDetailAPIView, CountryListAPIView, ProductImageModelAPIView, ProductDiscountAPIView, \
    ReviewModelSerializerListAPIView, AddRatingViewSet
from user.views import edit_account_view, update_username, update_phone, update_email, update_date, \
    update_male
from orders.views import user_order_view
from .yasg import urlpatterns as doc_urls


router = DefaultRouter()
router.register(r'add-rating', AddRatingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('products/', include('products.urls',  namespace='product')),
    path('about/', AboutTemplateView.as_view(), name='abouts'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
    path('articles/', HelpListView.as_view(), name='articles'),
    path('order/', OrderTemplateView.as_view(), name='order'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('profile/<int:user_pk>', user_order_view, name='profile'),
    path('profilw_edit/<user_id>/edit/', edit_account_view, name='edit'),
    path('change_username/<user_id>/edit/', update_username, name='update_username'),
    path('change_phone/<user_id>/edit/', update_phone, name='update_phone'),
    path('change_email/<user_id>/edit/', update_email, name='update_email'),
    path('change_date/<user_id>/edit/', update_date, name='update_date'),
    path('change_male/<user_id>/edit/', update_male, name='update_male'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('load-more-data/', load_more_data, name='load_more_data'),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/products/', ProductListAPIView.as_view()),
    path('api/v1/discount/', ProductDiscountAPIView.as_view()),
    path('api/v1/cities/', CountryListAPIView.as_view()),
    path('api/v1/reviews/<int:pk>', ReviewModelSerializerListAPIView.as_view()),
    path('api/v1/reviews/<int:pk>', ReviewModelSerializerListAPIView.as_view()),
    path('users/', include('user.urls')),
    path('api/v1/products/<int:pk>/', ProductDetailAPIView.as_view()),
    path('api/v1/carousels', CarouselListAPIView.as_view()),
    path('api/v1/help', HelpListAPIView.as_view()),
    path('api/v1/categories', CategoryListAPIView.as_view()),
    path('', HomeTemplate.as_view())
]

urlpatterns += doc_urls
urlpatterns += router.urls

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)