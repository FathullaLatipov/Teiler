from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import AuthViewSet, UserViewSet, UserDetailAPIView, UserProductDetail, UpdateProfileView, \
        GetProfileView, LogoutView, MyTokenObtainPairView, AddressInfoView, AddressProfileView, \
        DeleteAddressProfileView, SingelAddresInfoView

router = DefaultRouter()
# router.register('api/v1/auth', AuthViewSet, 'auth')
# router.register('api/v1/signup', UserViewSet, 'signup')

urlpatterns = [
        path('api/v1/lk/user/<int:pk>', UserDetailAPIView.as_view()),
        path('api/v1/lk/user/products/<int:pk>', UserProductDetail.as_view()),
        path('api/v1/editUser/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
        path('api/v1/getUser/<int:pk>/', GetProfileView.as_view(), name='getUser'),
        path('api/v1/address/', AddressInfoView.as_view(), name='address'),
        path('api/v1/address/<int:pk>/', SingelAddresInfoView.as_view(), name='address-si'),
        path('api/v1/address/update/<int:pk>/', AddressProfileView.as_view(), name='address-up'),
        path('api/v1/address/delete/<int:pk>/', DeleteAddressProfileView.as_view(), name='address-del'),
        path('', include(router.urls), name='signup'),
]