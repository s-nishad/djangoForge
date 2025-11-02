import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 

from apps.core.models import BaseModel
from config.settings import USE_ROLE

class UserRole(models.TextChoices):
    USER = "USER", "User"
    ADMIN = "ADMIN", "Admin" 
    # Add more roles if needed

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        
        if not password:
            raise ValueError("Password must be provided")
        
        email = self.normalize_email(email)
        if USE_ROLE and role is None:
            raise ValueError("Role is required when USE_ROLE is True")
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        role = extra_fields.pop('role', UserRole.ADMIN)
        return self.create_user(email, password, role=role, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True) 
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(
        max_length=30,
        choices=UserRole.choices,
        null=True,
        blank=True,
        default=UserRole.USER,
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    provided_name = models.CharField(max_length=150, blank=True, null=True)
    telegram_id = models.CharField(max_length=50, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
