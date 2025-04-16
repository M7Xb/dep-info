from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import base64
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),  # Added admin role
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    
    class Meta:
        db_table = 'auth_user'  # Specify the correct table name
        
    def __str__(self):
        return self.email
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='dashboard_user_groups',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='dashboard_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )
    profile_image_data = models.BinaryField(null=True, blank=True)
    profile_image_type = models.CharField(max_length=20, null=True, blank=True)

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def get_all_groups_id(cls):
        return 1  # ID of the "All Groups" group

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class TimeTable(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='timetables')
    pdf_data = models.BinaryField(null=True, blank=True)  # Allow null initially
    pdf_name = models.CharField(max_length=255, null=True, blank=True)  # Allow null initially
    uploaded_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Timetable for {self.group.name}"

    def get_pdf_url(self):
        """Generate a data URL for the PDF"""
        if self.pdf_data:
            pdf_base64 = base64.b64encode(self.pdf_data).decode('utf-8')
            return f"data:application/pdf;base64,{pdf_base64}"
        return None












