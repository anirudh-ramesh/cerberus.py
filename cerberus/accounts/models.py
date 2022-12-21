from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.gis.db import models
from base.models import BaseModel
from accounts.managers import UserManager



class User(
    AbstractBaseUser,
    BaseModel,
    PermissionsMixin,
):
    """
    Model class to hold all the user related data

    Users are people who can login on the platform and interact with it
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    first_name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )

    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
    )

    failed_login_attempts = models.IntegerField(default=0)

    is_locked = models.BooleanField(default=False)

    locked_date = models.DateTimeField(null=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
