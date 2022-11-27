from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import AuthViewSet, UserViewSet, UserDetailAPIView, UserProductDetail, UpdateProfileView, \
        GetProfileView, LogoutView, MyTokenObtainPairView, AddressInfoView

router = DefaultRouter()
# router.register('api/v1/auth', AuthViewSet, 'auth')
# router.register('api/v1/signup', UserViewSet, 'signup')

urlpatterns = [
        path('api/v1/lk/user/<int:pk>', UserDetailAPIView.as_view()),
        path('api/v1/lk/user/products/<int:pk>', UserProductDetail.as_view()),
        path('api/v1/editUser/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
        path('api/v1/getUser/<int:pk>/', GetProfileView.as_view(), name='getUser'),
        path('api/v1/address/', AddressInfoView.as_view(), name='address'),
        path('', include(router.urls), name='signup'),
]