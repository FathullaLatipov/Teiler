from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from rest_framework import generics, status, viewsets, serializers
from django.views.generic import CreateView, TemplateView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView

from user.forms import CustomUserCreationForm, CustomUserChangeForm, UserNameChangeForm, PhoneChangeForm, \
    EmailChangeForm, DateBrithChangeForm, MaleChangeForm
from user.models import CustomUser
from user.serializers import RegistrationSerializer, LoginSerializer, UserSerializer, \
    MyTokenObtainPairSerializer


# new new

class AuthViewSet(GenericViewSet):
    serializer_class = AuthTokenSerializer
    queryset = CustomUser.objects.all()


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    ordering = ['-date_joined']
    search_fields = ['username']
    serializer_class = RegistrationSerializer

    def create(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True})
        else:
            return Response({"status": False})


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    edit_user = CustomUser.objects.get(pk=user_id)
    if edit_user.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("/", user_id=edit_user.pk)
        else:
            form = CustomUserChangeForm(request.POST, instance=request.user,
                                        initial={
                                            "id": edit_user.pk,
                                            "phone": edit_user.phone,
                                        }
                                        )
            context['form'] = form
    else:
        form = CustomUserChangeForm(
            initial={
                "id": edit_user.pk,
                "phone": edit_user.phone,
            }
        )
        context['form'] = form
    return render(request, "edit_all.html", context)


def update_username(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user = CustomUser.objects.get(pk=user_id)
    context = {}

    if request.POST:
        form = UserNameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/', user_id=user.id)

        else:
            form = UserNameChangeForm(request.POST, instance=request.user)
            context['form'] = form

    return render(request, 'lk.html', context)


def update_phone(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user = CustomUser.objects.get(pk=user_id)
    context = {}

    if request.POST:
        form = PhoneChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/', user_id=user.id)

        else:
            form = PhoneChangeForm(request.POST, instance=request.user)
            context['form'] = form

    return render(request, 'lk.html', context)


def update_email(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user = CustomUser.objects.get(pk=user_id)
    context = {}

    if request.POST:
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/', user_id=user.id)

        else:
            form = EmailChangeForm(request.POST, instance=request.user)
            context['form'] = form

    return render(request, 'lk.html', context)


def update_date(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user = CustomUser.objects.get(pk=user_id)
    context = {}

    if request.POST:
        form = DateBrithChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/', user_id=user.id)

        else:
            form = DateBrithChangeForm(request.POST, instance=request.user)
            context['form'] = form

    return render(request, 'lk.html', context)


def update_male(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user = CustomUser.objects.get(pk=user_id)
    context = {}

    if request.POST:
        form = MaleChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/', user_id=user.id)

        else:
            form = MaleChangeForm(request.POST, instance=request.user)
            context['form'] = form

    return render(request, 'lk.html', context)
