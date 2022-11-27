from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, AddressInfoModel


@admin.register(AddressInfoModel)
class AddressInfoModelAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class LomrenAdmin(admin.ModelAdmin):
    pass

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     list_display = ['pk', 'username', 'email', 'last_name', 'phone', 'is_staff']



