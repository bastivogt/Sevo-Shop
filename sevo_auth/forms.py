from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.utils.translation import gettext_lazy as _

from . import models

# class CustomUserCreateForm(UserCreationForm):
#     class Meta:
#         model = models.CustomUser
#         fields = UserChangeForm.Meta.fields

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = models.CustomUser
#         fields = UserChangeForm.Meta.fields


class SevoLoginForm(forms.Form):
    username = forms.CharField(max_length=255, label=_("Username"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"



class SevoSignUpForm(forms.Form):
    username = forms.CharField(max_length=255, label=_("Username"))
    email = forms.CharField(max_length=255, widget=forms.EmailInput, label=_("E-Mail"))

    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=_("Password confirm"), widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password_confirm"].widget.attrs["class"] = "form-control"





class SevoChangePasswordForm(forms.Form):
    password = forms.CharField(label=_("New password"), widget=forms.PasswordInput,)
    password_confirm = forms.CharField(label=_("New password confirm"), widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password_confirm"].widget.attrs["class"] = "form-control"


class SevoChangeUserDataForm(forms.Form):
    username = forms.CharField(max_length=255, label=_("Username"))
    email = forms.CharField(max_length=255, widget=forms.EmailInput, label=_("E-Mail"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"



class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=255, label=_("Username"))
    email = forms.CharField(max_length=255, widget=forms.EmailInput, label=_("E-Mail"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["class"] = "form-control"
