from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from help.views import HelpListView
from products.views import HomeTemplate, AboutTemplateView, ContactTemplateView
from user.views import ProfileView, edit_account_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('products/', include('products.urls',  namespace='product')),
    path('about/', AboutTemplateView.as_view(), name='abouts'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
    path('articles/', HelpListView.as_view(), name='articles'),
    path('accounts/', include('user.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profilw_edit/<user_id>/edit/', edit_account_view, name='edit'),
    path('', HomeTemplate.as_view())
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)