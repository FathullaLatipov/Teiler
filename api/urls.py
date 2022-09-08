from django.urls import path


from api.views import TestList

urlpatterns = [
    path('test/', TestList.as_view())
]
