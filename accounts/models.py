"""
Accounts App – Custom User Model with Role-Based Access
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
        ('cashier', 'Cashier'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_manager(self):
        return self.role in ['admin', 'manager'] or self.is_superuser

    @property
    def is_cashier(self):
        return self.role in ['admin', 'manager', 'cashier'] or self.is_superuser

    def get_avatar_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return None

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
