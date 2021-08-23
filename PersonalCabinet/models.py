from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserPrivacy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isPrivacy = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Приватность пользователя'
        verbose_name_plural = 'Приватность пользователей'
