from django.db import models
from django.contrib.auth.hashers import make_password


class UserAccount(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # will store hashed password

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email