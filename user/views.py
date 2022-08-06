from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.conf import settings
from user.forms import CustomUserCreationForm, CustomUserChangeForm, UserNameChangeForm
from user.models import CustomUser


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(TemplateView):
    template_name = 'lk.html'


def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    edit_user = CustomUser.objects.get(pk=user_id)
    edit_phone = CustomUser.objects.get(pk=user_id)
    edit_email = CustomUser.objects.get(pk=user_id)
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
                                            "username": edit_user.username,
                                            "email": edit_user.email,
                                        }
                                        )
            context['form'] = form
    else:
        form = CustomUserChangeForm(
            initial={
                "id": edit_user.pk,
                "phone": edit_user.phone,
                "username": edit_user.username,
                "email": edit_user.email,
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