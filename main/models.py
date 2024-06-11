from django_cryptography.fields import encrypt

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserManager(BaseUserManager):
    def create(self, phone_number, password=None, **exstra_field):
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        user = self.model(phone_number=phone_number,  **exstra_field)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=11, unique=True)
    invite_code = models.CharField(max_length=6, blank=True, null=True)
    inviter = models.ForeignKey('self', on_delete=models.CASCADE, related_name="invited", null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.phone_number


class SmsCode(models.Model):
    phone_number = models.CharField(max_length=11, db_index=True)
    date = models.DateTimeField(default=timezone.now, db_index=True)
    code = encrypt(models.CharField(max_length=4, db_index=True))
    used = models.BooleanField(default=False)


