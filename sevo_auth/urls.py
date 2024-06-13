from django.urls import path
from  . import views
from django.conf import settings



urlpatterns = [
    path("login/", views.login, name="sevo-auth-login"),
    path("logout", views.logout, name="sevo-auth-logout"),
    path("signup", views.sign_up, name="sevo-auth-sign-up"),
    path("user-detail", views.user_detail, name="sevo-auth-user-detail"),
    path("change-password", views.change_password, name="sevo-auth-change-password"),
    path("change-user-data", views.change_user_data, name="sevo-auth-change-user-data"),
    path("forgot-password", views.forgot_password, name="sevo-auth-forgot-password"),
    path("new-password/<str:token>", views.set_new_password_token, name="sevo-auth-set-new-password-token")
]


