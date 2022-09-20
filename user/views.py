from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import generics, status
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
from user.serializers import RegistrationSerializer, LoginSerializer, RegisterSerializer, UserSerializer, \
    MyTokenObtainPairSerializer


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# new new

class AuthViewSet(GenericViewSet):
    serializer_class = AuthTokenSerializer
    queryset = CustomUser.objects.all()


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = CustomUser.objects.all()
    ordering = ['-date_joined']
    search_fields = ['username']

# class RegisterView(generics.GenericAPIView):
#     serializer_class = RegistrationSerializer
#     model = CustomUser
#
#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#         user = CustomUser.objects.get(email=user_data['email'])
#         token = RefreshToken.for_user(user).access_token
#         # current_site = get_current_site(request).domain
#         # relativeLink = reverse('email-verify')
#         # absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
#         # email_body = 'Hi '+user.username + \
#         #     ' Use the link below to verify your email \n' + absurl
#         # data = {'email_body': email_body, 'to_email': user.email,
#         #         'email_subject': 'Verify your email'}
#         #
#         # Util.send_email(data)
#         return Response({"token": str(token)}, status=status.HTTP_201_CREATED)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully",
        })


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
