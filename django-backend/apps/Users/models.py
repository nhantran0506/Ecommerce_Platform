from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class UserRoles(models.TextChoices):
    USER = "USER", "User"
    ADMIN = "ADMIN", "Admin"
    SHOP_OWNER = "SHOP_OWNER", "Shop Owner"


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    address = models.CharField(max_length=255, null=True)
    dob = models.DateTimeField(null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10,
        choices=UserRoles.choices,
        default=UserRoles.USER
    )
    deleted_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'users'


class Authentication(models.Model):
    class ProviderEnum(models.TextChoices):
        DEFAULT = "website", "Website"
        GOOGLE_PROVIDER = "google", "Google"
        FACEBOOK_PROVIDER = "facebook", "Facebook"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='authenticate')
    user_name = models.CharField(max_length=255, unique=True)
    hash_pwd = models.CharField(max_length=255, null=True)
    temp_code = models.CharField(max_length=255, null=True)
    temp_code_expiration = models.DateTimeField(null=True)
    provider_user_id = models.CharField(max_length=255, null=True)
    provider = models.CharField(
        max_length=20,
        choices=ProviderEnum.choices,
        default=ProviderEnum.DEFAULT
    )

    class Meta:
        db_table = 'authentication' 