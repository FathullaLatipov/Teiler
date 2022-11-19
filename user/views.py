from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, viewsets, serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from djoser import utils
from djoser.conf import settings
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from orders.models import OrderItem
from products.models import ProductModel
from products.serializers import ProductDetailSerializer
from user.forms import CustomUserChangeForm, UserNameChangeForm, PhoneChangeForm, \
    EmailChangeForm, DateBrithChangeForm, MaleChangeForm
from user.models import CustomUser
from user.serializers import RegistrationSerializer, LoginSerializer, MyTokenObtainPairSerializer, UserOrderSerializer, \
    UpdateUserSerializer, UserInfoSerializer


# new new

class AuthViewSet(GenericViewSet):
    serializer_class = AuthTokenSerializer
    queryset = CustomUser.objects.all()

    @action(['DELETE'], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request: Request):
        Token.objects.get(user=request.user).delete()
        data = {'status': 'Successfully log outed user'}
        return Response(status=status.HTTP_204_NO_CONTENT, data=data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Logout(POST)",
        operation_description="Метод для Logout",
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# #
# @action(['POST'], detail=False, permission_classes=[permissions.AllowAny])
# def login(self, request: Request):
#     self.serializer_class = AuthTokenSerializer
#     serializer = self.get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.validated_data['user']
#     token, created = Token.objects.get_or_create(user=user.id)
#     return Response({'token': token.key, 'message': 'Success'})
# {'message':'sucess','error':False,'code':200,'result':{'totalItems':len(serializer.data),'items':serializer.data,'totalPages':'null','currentPage':0}}
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


class UserDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Получения данных пользователья(ЛК)",
        operation_description="Метод получения данных пользователья. Помимо типа данных и токен авторизации, передаётся только ID пользователья.",
    )
    def get(self, request, pk):
        users = CustomUser.objects.get(id=pk)
        serializer = RegistrationSerializer(users, context={'request': request})
        return Response(serializer.data)


class UserProductDetail(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Получения данных товаров пользователья(ЛК)",
        operation_description="Метод получения товаров пользователья. Помимо типа данных и токен авторизации, передаётся только ID заказа(ID заказа отображается на админке и оно генирируется сам) после оформления заказа.",
    )
    def get(self, request, pk):
        products = OrderItem.objects.get(order=pk)
        serializer = UserOrderSerializer(products, context={'request': request})
        return Response(serializer.data)


# class UserProductDetail(ListAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = UserOrderSerializer

class LoginAPIView(generics.GenericAPIView):
    ''' Логин юзера '''
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):
    serializer_class = settings.SERIALIZERS.token_create
    permission_classes = settings.PERMISSIONS.token_create
    print(serializer_class)
    print(permission_classes)

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        print(token)
        print(serializer.user, 'user')
        return Response(
            data=token_serializer_class(token).data,
            exception=serializer.user,
            status=status.HTTP_200_OK
        )


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


class UpdateProfileView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class GetProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        operation_summary="Принимает обновленные данные пользователя",
        operation_description="Метод для того что бы показать обновленные данные пользователя.В запросе надо в конце писать ID(Пользователя)",
    )
    def get(self, request, pk):
        users = CustomUser.objects.get(pk=pk)
        serializer = UserInfoSerializer(users, context={'request': request})
        return Response(serializer.data)


class MyTokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()
