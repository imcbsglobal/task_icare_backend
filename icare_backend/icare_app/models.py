# icare_app/models.py
from django.db import models
from django.contrib.auth.models import User

class Registration(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history', null=True, blank=True)
    username = models.CharField(max_length=150)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='success')

    class Meta:
        ordering = ['-login_time']
        verbose_name_plural = "Login Histories"

    def __str__(self):
        return f"{self.username} - {self.login_time.strftime('%Y-%m-%d %H:%M:%S')}"


class Showcase(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    media_file = models.FileField(upload_to='showcase/')
    website_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# NEW MODEL FOR DEMONSTRATION
class Demonstration(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    media_file = models.FileField(upload_to='demonstration/')
    website_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title