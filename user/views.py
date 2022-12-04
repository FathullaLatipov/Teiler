from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, viewsets, serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from djoser import utils
from djoser.conf import settings
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from orders.models import OrderItem
from products.models import ProductModel
from products.serializers import ProductDetailSerializer
from user.filters import ModelFilter
from user.forms import CustomUserChangeForm, UserNameChangeForm, PhoneChangeForm, \
    EmailChangeForm, DateBrithChangeForm, MaleChangeForm
from user.models import CustomUser, AdressInfoModel
from user.serializers import RegistrationSerializer, LoginSerializer, MyTokenObtainPairSerializer, UserOrderSerializer, \
    UpdateUserSerializer, UserInfoSerializer, NewUserSerializer, AddressCreateSerializer, AddresUserSerializer, \
    DeleteAddresUserSerializer

# new new
from user.utils import generate_access_token, generate_refresh_token


class AuthViewSet(GenericViewSet):
    serializer_class = AuthTokenSerializer
    queryset = CustomUser.objects.all()

    @action(['DELETE'], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request: Request):
        Token.objects.get(user=request.user).delete()
        data = {'status': 'Successfully log outed user'}
        return Response(status=status.HTTP_204_NO_CONTENT, data=data)


# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     @swagger_auto_schema(
#         operation_summary="Logout(POST)",
#         operation_description="Метод для Logout",
#     )
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#
#             return Response({"Success": "Упешно"}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({"Success": "Ошибка"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        if not token.blacklist():
            return Response("Ошибка")
        else:
            return Response({"status": "Успешно"})


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


class UserViewSet(generics.CreateAPIView):
    ''' Регистрация юзера '''
    queryset = CustomUser.objects.all()
    ordering = ['-date_joined']
    search_fields = ['username']
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True})
        else:
            return Response(serializer.errors)
    # def create(self, request):
    #     serializer = RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"status": True})
    #     else:
    #         return Response(serializer.errors)


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


# class MyAPIViewKlass(APIView):
#     filter_backends = (filters.DjangoFilterBackend,)
#
#     def filter_queryset(self, queryset):
#         for backend in list(self.filter_backends):
#             queryset = backend().filter_queryset(self.request, queryset, self)
#         return queryset
#
#     def get(self, request, *args, **kwargs):
#         base_qs = MyModel.objects.all()
#         filtered_qs = self.filter_queryset(base_qs)
#         serializer = MySerializer(filtered_qs, many=True)
#         return Response(serializer.data)
# class UserProductDetail(APIView):
#     permission_classes = (AllowAny,)
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['price']
#
    # @swagger_auto_schema(
    #     operation_summary="Получения данных товаров пользователья(ЛК)",
    #     operation_description="Метод получения товаров пользователья. Помимо типа данных и токен авторизации, передаётся только ID заказа(ID заказа отображается на админке и оно генирируется сам) после оформления заказа.",
    # )
#     def get(self, request, pk):
#         products = OrderItem.objects.get(order=pk)
#         serializer = UserOrderSerializer(products, context={'request': request})
#         return Response(serializer.data)


class UserProductDetail(generics.ListAPIView):
    serializer_class = UserOrderSerializer
    queryset = OrderItem.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product__status']

    @swagger_auto_schema(
        operation_summary="Получения данных товаров пользователья(ЛК)",
        operation_description="Метод получения товаров пользователья. Помимо типа данных и токен авторизации, передаётся только ID заказа(ID заказа отображается на админке и оно генирируется сам) после оформления заказа.",
    )
    def get_queryset(self):
        pk = self.kwargs['pk']
        return self.queryset.filter(
            order_id=pk
        )

#     def get_queryset(self):
#         """
#         This view should return a list of all models by
#         the maker passed in the URL
#         """
#         maker = self.kwargs['make']
#         return Model.objects.filter(make=maker)

# class CollectionVideoViewSet(ListAPIView):
#     """ViewSet for operation with videos in collection"""
#     permission_classes = (IsAuthenticated,)
#     queryset = Video.objects.all()
#     serializer_class = CollectionVideoSerializer
#
#     def get_queryset(self):
#         # Assuming your `Video` model has a many-to-one relation to `Collection`
#         return self.queryset.filter(
#             collection__pk=self.kwargs['pk']
#         )


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
    permission_classes = (AllowAny,)
    serializer_class = UpdateUserSerializer


class GetProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Принимает обновленные данные пользователя",
        operation_description="Метод для того что бы показать обновленные данные пользователя.В запросе надо в конце писать ID(Пользователя)",
    )
    #  def to_internal_value(self, validated_data):
    #         raw_password = validated_data.pop('password')
    #         user = super().to_internal_value(validated_data)
    #         user.set_password(raw_password)  # Hash the raw password
    #         return user
    def get(self, request, pk):
        users = CustomUser.objects.get(pk=pk)
        # password = request.GET.get('password'),
        # print(password, 'passs')
        #  make_password(users.password),
        serializer = UserInfoSerializer(users, context={'request': request})
        return Response(serializer.data)


class MyTokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


class UserNewCreateView(generics.CreateAPIView):
    serializer_class = NewUserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        response = Response()

        user = CustomUser.objects.filter(username=username).first()
        if (user is None):
            raise AuthenticationFailed('Имя пользователья обязательное поле')
        if (not user.check_password(password)):
            raise AuthenticationFailed('нужен password')

        serialized_user = NewUserSerializer(user).data

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'user': serialized_user,
        }

        return response


class SingelAddresInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Один обьект адрес (GET)(ID)",
        operation_description="Метод для того что бы показать данные адреса.В запросе надо в конце писать ID(адреса)",
    )
    def get(self, request, pk):
        address = AdressInfoModel.objects.get(pk=pk)
        # password = request.GET.get('password'),
        # print(password, 'passs')
        #  make_password(users.password),
        serializer = AddressCreateSerializer(address, context={'request': request})
        return Response(serializer.data)


class AddressInfoView(ListAPIView):
    queryset = AdressInfoModel.objects.all()
    serializer_class = AddressCreateSerializer

    @swagger_auto_schema(
        operation_summary="Получения всех адресов(GET)",
        operation_description="Метод для того что бы получать все данные(Адрес)",
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AddressCreateSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Создание адресов(POST)",
        operation_description="Метод для того что бы создать данные(Адрес)",
    )
    def post(self, request):
        reviews = AdressInfoModel.objects.create(
            address=request.data['address'],
            lat=request.data['lat'],
            lng=request.data['lng'],
            is_house=request.data['is_house'],
            comment=request.data['comment'],
        )

        return Response(self.serializer_class(reviews, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)


class AddressProfileView(generics.UpdateAPIView):
    queryset = AdressInfoModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AddresUserSerializer


class DeleteAddressProfileView(generics.DestroyAPIView):
    queryset = AdressInfoModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = DeleteAddresUserSerializer
