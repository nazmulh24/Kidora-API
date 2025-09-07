from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager

from cloudinary.models import CloudinaryField
from product.validators import validate_file_size


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    profile_picture = CloudinaryField(
        "image",
        blank=True,
        null=True,
        validators=[validate_file_size],
        folder="Kidora/users/profile_pictures",
    )
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = "email"  # ---> Use email instead of username
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
