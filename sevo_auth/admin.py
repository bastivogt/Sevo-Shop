from django.contrib import admin

# Register your models here.
from . import models


class PasswordForgotTokenAdmin(admin.ModelAdmin):
    
    list_display = [
        "user",
        "token"
    ]


admin.site.register(models.PasswordResetToken, PasswordForgotTokenAdmin)
