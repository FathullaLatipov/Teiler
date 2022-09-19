from django.urls import path

from user.views import SignupView, RegisterView, LoginAPIView

urlpatterns = [
        path('signup/', RegisterView.as_view(), name='signup'),
        path('login/', LoginAPIView.as_view(), name="login"),
]