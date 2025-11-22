"""
Models for the users app.
This defines the TUser model that maps to the t_users table in MySQL.
"""
from django.db import models
import logging

logger = logging.getLogger(__name__)


class TUser(models.Model):
    """
    Model representing the t_users table in the database.
    Django will use this to map to the existing t_users table.

    Note: This model maps to an existing MySQL table with 'name' column
    instead of separate first_name/last_name columns.
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)  # Single name field (matches existing DB)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_users'
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.email})"

    def save(self, *args, **kwargs):
        """Override save to add logging."""
        if self.pk:
            logger.info(f"Updating user: {self.username}")
        else:
            logger.info(f"Creating new user: {self.username}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Override delete to add logging."""
        logger.info(f"Deleting user: {self.username}")
        super().delete(*args, **kwargs)
