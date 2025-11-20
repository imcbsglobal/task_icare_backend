from django.contrib import admin
from .models import Registration, Showcase, LoginHistory, Demonstration

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'phone', 'email']

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['username', 'login_time', 'ip_address', 'status']
    list_filter = ['status', 'login_time']
    search_fields = ['username', 'ip_address']
    readonly_fields = ['user', 'username', 'login_time', 'ip_address', 'user_agent', 'status']

@admin.register(Showcase)
class ShowcaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']

@admin.register(Demonstration)
class DemonstrationAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']