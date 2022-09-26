from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import AuthViewSet, LoginView, UserViewSet

router = DefaultRouter()
router.register('api/v1/auth', AuthViewSet, 'auth')
router.register('api/v1/signup', UserViewSet, 'signup')

urlpatterns = [
        path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
        path('login/', LoginView.as_view(), name="login"),
        path('', include(router.urls), name='signup'),
]