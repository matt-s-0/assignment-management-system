from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    displayName = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def getDisplayName(self):
        return self.displayName
    
    def getUserFromEmail(self, email):
        try:
            normalizedEmail = self.normalizeEmail(email)
            return self.get(email=normalizedEmail)
        except self.model.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        if not self.displayName:
            self.displayName = self.username
        super().save(*args, **kwargs)