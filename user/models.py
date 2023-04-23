import os
import uuid

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


def create_custom_path(instance, filename):
    _, ext = os.path.splitext(filename)
    filename = f"{slugify(instance.username)}-{uuid.uuid4()}{ext}"
    return os.path.join("avatars/", filename)


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        FEMALE = "Female"
        MALE = "Male"
        NON_BINARY = "Non-binary"

    username = models.CharField(max_length=63)
    email = models.EmailField("email address", unique=True)
    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=23, choices=GenderChoices.choices, null=True, blank=True
    )
    avatar = models.ImageField(null=True, blank=True, upload_to=create_custom_path)
    followed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="who_follow_me",
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
