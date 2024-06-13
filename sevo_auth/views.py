from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.conf import settings


from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings

from . import forms
from . import helpers
from . import models

from django.utils.translation import gettext_lazy as _




# Create your views here.


# def login(request):
#     if request.method  == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         url = reverse("sevo-auth-login")
        
#         if user is not None:
#             auth_login(request, user)
#             messages.add_message(request, messages.SUCCESS, _("login_success_msg"))
#             return HttpResponseRedirect(url)
#         else:
#             messages.add_message(request, messages.ERROR, _("login_failed_msg"))

    
#     return render(request, "sevo_auth/login.html", {
#         "title": _("login_title")
#     })


# logout
def logout(request):
    if settings.SEVO_AUTH_LOGOUT_REDIRECT:
        url = reverse(settings.SEVO_AUTH_LOGOUT_REDIRECT)
    else:
        url = reverse("sevo-auth-login")


    auth_logout(request)
    messages.add_message(request, messages.SUCCESS, _("You are logged out!"))
    return HttpResponseRedirect(url)



# login
def login(request):
    if settings.SEVO_AUTH_LOGIN_REDIRECT:
        url = reverse(settings.SEVO_AUTH_LOGIN_REDIRECT)
    else:
        url = reverse("sevo-auth-user-detail")

    if request.method == "POST":
        form = forms.SevoLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.add_message(request, messages.SUCCESS, _("You are logged in!"))
                return HttpResponseRedirect(url)
            else:
                messages.add_message(request, messages.ERROR, _("Login failed!"))   
                return HttpResponseRedirect(url)
    else:
        form = forms.SevoLoginForm()
    return render(request, "sevo_auth/login.html", {
        "title": _("Login"),
        "form": form,
        "can_sign_up": settings.SEVO_AUTH_CAN_SIGN_UP
    })


# sign_up
def sign_up(request):
    if settings.SEVO_AUTH_CAN_SIGN_UP:
        if request.method == "POST":
            form = forms.SevoSignUpForm(request.POST)
            if form.is_valid():
                print("form valid")
                email = form.cleaned_data["email"]
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                password_confirm = form.cleaned_data["password_confirm"]



                if password != password_confirm:
                    messages.add_message(request, messages.ERROR, _("Failed password confirm!"))
                else:
                    try:
                        user = User(username=username, email=email)
                        user.set_password(password)
                        user.save()
                        messages.add_message(request, messages.SUCCESS, _("You are signed up!"))
                        url = reverse("sevo-auth-user-detail")
                        return HttpResponseRedirect(url) 
                    except IntegrityError as e:
                        messages.add_message(request, messages.ERROR, _("Failed, username allready exists!"))
                    
        else:
            form = forms.SevoSignUpForm()
        
        return render(request, "sevo_auth/sign_up.html", {
            "title": _("Sign up"),
            "form": form
        })
    else:
        url = reverse("sevo-auth-login")
        return HttpResponseRedirect(url)


# user_detail
@login_required(login_url="sevo-auth-login")
def user_detail(request):
    current_user = request.user
    greeting_word = _("Hello")
    greeting = f"{greeting_word}, {current_user.username}!"
    return render(request, "sevo_auth/user_detail.html", {
        "greeting": greeting,
        "user": current_user
    })


# change_password
@login_required(login_url="sevo-auth-login")
def change_password(request):
    current_user = request.user
    if request.method == "POST":
        form = forms.SevoChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            password_confirm = form.cleaned_data["password_confirm"]
            if(password != password_confirm):
                messages.add_message(request, messages.ERROR, _("Change password failed!"))
                # url = reverse("sevo-auth-change-password")
                # return HttpResponseRedirect(url)
            else:
                current_user.set_password(password)
                current_user.save()
                messages.add_message(request, messages.SUCCESS, _("Change password successful!"))
                url = reverse("sevo-auth-logout")
                return HttpResponseRedirect(url)

                # url = reverse("sevo-auth-user-detail")
                # return HttpResponseRedirect(url)
    else:
        form = forms.SevoChangePasswordForm()

    return render(request, "sevo_auth/change_password.html", {
        "title": _("Change password"),
        "form": form
    })

# change_user_data
@login_required(login_url="sevo-auth-login")
def change_user_data(request):
    current_user = request.user
    inital_data = {
        "username": current_user.username,
        "email": current_user.email,
    }
    if request.method == "POST":
        form = forms.SevoChangeUserDataForm(request.POST, initial=inital_data)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            current_user.username = username
            current_user.email = email
            if current_user.check_password(password):
                try:
                    current_user.save()
                    messages.add_message(request, messages.SUCCESS, _("Userdata successful changed!"))

                    url = reverse("sevo-auth-user-detail")
                    return HttpResponseRedirect(url)
                except IntegrityError as e:
                    messages.add_message(request, messages.ERROR, _("Failed, username allready exists!"))
                    url = reverse("sevo-auth-change-user-data")
                    return HttpResponseRedirect(url)
            
            else:
                messages.add_message(request, messages.ERROR, _("Failed, wrong password!"))


    else:
        form = forms.SevoChangeUserDataForm(initial=inital_data)
    return render(request, "sevo_auth/change_user_data.html", {
        "title": _("Change userdata"),
        "form": form
    })



# forgot_password
def forgot_password(request):
    success = False
    if request.method == "POST":
        form = forms.ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            try:
                user = User.objects.get(username=username, email=email)
                token_str = helpers.create_token()
                print(f"Token: {token_str}")
                try:
                    token = models.PasswordResetToken.objects.get(user=user)
                    token.token = token_str
                except:
                    token = models.PasswordResetToken(user=user, token=token_str)
                
                print(token)
                token.save()
                print(user)

                # send token link per mail


                success = True
                

            except:
                # url = reverse("sevo-auth-forgot-password")
                # return HttpResponseRedirect(url)
                success = False


        print(f"success: {success}") 
        if success:
            messages.add_message(request, messages.SUCCESS, _("Please, check your e-mails!"))
            url = reverse("sevo-auth-set-new-password-token", args=[token_str])
            response = HttpResponseRedirect(url)
            domain = request.build_absolute_uri('/')[:-1]
            link = f"{domain}{response.url}"
            print("###############################################")
            print(f"Resetlink per Mail: {link}")
            print("###############################################")

            send_mail(
                    _("SEVO Vereinsmanager Passwordreset"),
                    f"Resetlink: {link}",
                    #settings.EMAIL_HOST_USER,
                    settings.SEVO_AUTH_DEFAULT_FROM_MAIL,
                    [user.email],
                    fail_silently=False,
                )
            url = reverse("sevo-auth-forgot-password")
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, _("Username not found"))
            url = reverse("sevo-auth-forgot-password")
            return HttpResponseRedirect(url)


    else:
        form = forms.ForgotPasswordForm()

    return render(request, "sevo_auth/forgot_password.html", {
        "title": _("Forgot password"),
        "form": form
    })



def set_new_password_token(request, token):
    the_token = get_object_or_404(models.PasswordResetToken, token=token)
    if request.method == "POST":
        form = forms.SevoSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            password_confirm = form.cleaned_data.get("password_confirm")

            user_exist = False

            if password != password_confirm:
                messages.add_message(request, messages.ERROR, _("Fail, password not confirm!"))
                url = reverse("sevo-auth-set-new-password-token")
                return HttpResponseRedirect(url)
            
            try:
                user = User.objects.get(username=username, email=email)
                user.set_password(password)
                user.save()
                the_token.delete()
                user_exist = True
                user_exist = True
            except:
                user_exist = False
            

            if user_exist:
                messages.add_message(request, messages.SUCCESS, _("Password changed!"))
                url = reverse("sevo-auth-login")
                return HttpResponseRedirect(url)
            else:
                messages.add_message(request, messages.ERROR, _("Fail, something went wrong!"))
    else:
        form = forms.SevoSignUpForm()

    return render(request, "sevo_auth/set_new_password_token.html", {
        "title": _("Set new password"), 
        "form": form
    })




    