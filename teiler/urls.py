from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from help.views import HelpListView
from products.views import HomeTemplate, AboutTemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('products/', include('products.urls',  namespace='product')),
    path('about/', AboutTemplateView.as_view()),
    path('articles/', HelpListView.as_view()),
    path('', HomeTemplate.as_view())
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)