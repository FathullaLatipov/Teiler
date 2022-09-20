from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import SignupView, LoginAPIView, RegisterAPI, AuthViewSet, LoginView, UserViewSet

router = DefaultRouter()
router.register('auth', AuthViewSet, 'auth')
router.register('users', UserViewSet, 'users')

urlpatterns = [
        # path('signup/', RegisterView.as_view(), name='signup'),
        path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
        path('login/', LoginView.as_view(), name="login"),
        path('', include(router.urls)),
]