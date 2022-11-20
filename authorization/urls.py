from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import MyTokenObtainPairView, LogoutView, UserViewSet

urlpatterns = [
    path('api/token/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/log', UserNewCreateView.as_view(), name='login'),
    path('api/token/logout', LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/signup/', UserViewSet.as_view(), name='signup'),
]