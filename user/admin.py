from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, AdressInfoModel


@admin.register(AdressInfoModel)
class AdressInfoModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'address', 'created_at']


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['pk', 'username', 'email', 'last_name', 'phone', 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)
