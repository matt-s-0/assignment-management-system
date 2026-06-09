from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    displayName = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def getDisplayName(self) -> str | None:
        return self.displayName

    def save(self, *args, **kwargs) -> None:
        if not self.displayName:
            self.displayName = self.username
        super().save(*args, **kwargs)