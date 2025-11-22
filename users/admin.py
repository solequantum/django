"""
Admin configuration for users app.
Registers the TUser model in Django admin interface.
"""
from django.contrib import admin
from .models import TUser


@admin.register(TUser)
class TUserAdmin(admin.ModelAdmin):
    """Admin interface for TUser model."""

    list_display = ['id', 'username', 'email', 'name', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['username', 'email', 'name', 'phone']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'name')
        }),
        ('Contact Information', {
            'fields': ('phone',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
