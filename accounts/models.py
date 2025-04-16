from django.contrib.auth.models import AbstractUser
from django.db import models
import base64

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    profile_image_data = models.BinaryField(null=True, blank=True)
    profile_image_type = models.CharField(max_length=255, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        if self.is_staff or self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['email']

    def get_profile_image_url(self):
        if self.profile_image_data and self.profile_image_type:
            base64_image = base64.b64encode(self.profile_image_data).decode('utf-8')
            return f"data:{self.profile_image_type};base64,{base64_image}"
        return None
