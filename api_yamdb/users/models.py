from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_username

NAME_MAX_LENGTH: int = 150
ROLE_MAX_LENGTH: int = 20
EMAIL_MAX_LENGTH: int = 254
CODE_MAX_LENGTH: int = 255


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    username = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        blank=False,
        null=False,
        validators=[validate_username]
    )
    first_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        blank=True
    )
    role = models.CharField(
        choices=ROLES,
        default=USER,
        max_length=ROLE_MAX_LENGTH
    )
    email = models.EmailField(unique=True, max_length=EMAIL_MAX_LENGTH)
    confirmation_code = models.CharField(
        max_length=CODE_MAX_LENGTH,
        null=True,
        blank=False,
        default='XXXX'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user_email'
            )
        ]

    def __str__(self):
        return self.username

    def clean(self) -> None:
        if self.is_superuser:
            self.role = self.ROLES.ADMIN
