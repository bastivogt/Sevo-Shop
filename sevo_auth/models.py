from django.db import models

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.





class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    token = models.CharField(max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)


    def get_token_piece(self, length=7):
        temp = ""
        for c in range(length):
            temp += self.token[c]
        return temp

    def __str__(self):
        return f"{self.user.username} - {self.token}"
