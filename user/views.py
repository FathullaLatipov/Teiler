
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import generics, status, viewsets, serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.request import Request

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.forms import CustomUserChangeForm, UserNameChangeForm, PhoneChangeForm, \
    EmailChangeForm, DateBrithChangeForm, MaleChangeForm
from user.models import CustomUser
from user.serializers import RegistrationSerializer, LoginSerializer, MyTokenObtainPairSerializer


# new new

class AuthViewSet(GenericViewSet):
    serializer_class = AuthTokenSerializer
    queryset = CustomUser.objects.all()

    #
    # @action(['POST'], detail=False, permission_classes=[permissions.AllowAny])
    # def login(self, request: Request):
    #     self.serializer_class = AuthTokenSerializer
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response({'token': token.key})
    #
    # #
    # @action(['DELETE'], detail=False, permission_classes=[IsAuthenticated])
    # def logout(self, request: Request):
    #     Token.objects.get(user=request.user).delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # @action(['POST'], detail=False, permission_classes=[permissions.AllowAny])
    # def login(self, request: Request):
    #     self.serializer_class = MyTokenObtainPairSerializer
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     token = serializer.validated_data['access']
    #     return Response({'token': token})


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    ''' Регистрация юзера '''
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
            return Response(serializer.errors)


class LoginAPIView(generics.GenericAPIView):
    ''' Логин юзера '''
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
