"""
Serializers for the users app.
These convert model instances to JSON and validate input data.
"""
from rest_framework import serializers
from .models import TUser


class TUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the TUser model.
    Handles conversion between TUser instances and JSON.
    """

    class Meta:
        model = TUser
        fields = [
            'id',
            'username',
            'email',
            'name',
            'phone',
            'address',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        """Validate email field."""
        if value:
            value = value.lower()
        return value

    def validate_username(self, value):
        """Validate username field."""
        if value and len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        return value
