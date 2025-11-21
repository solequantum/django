"""
Views for the users app.
Implements CRUD operations for the TUser model via REST API.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from .models import TUser
from .serializers import TUserSerializer

logger = logging.getLogger(__name__)


class TUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TUser model providing CRUD operations.

    list: Get all users with pagination
    create: Create a new user
    retrieve: Get a specific user by ID
    update: Update a user completely
    partial_update: Update a user partially
    destroy: Delete a user
    """
    queryset = TUser.objects.all()
    serializer_class = TUserSerializer

    @swagger_auto_schema(
        operation_description="Get list of all users with pagination",
        responses={200: TUserSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List all users with pagination."""
        logger.info("Fetching user list")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=TUserSerializer,
        responses={
            201: TUserSerializer,
            400: 'Bad Request'
        }
    )
    def create(self, request, *args, **kwargs):
        """Create a new user."""
        logger.info(f"Creating new user with data: {request.data}")
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"User created successfully: {response.data.get('username')}")
            return response
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise

    @swagger_auto_schema(
        operation_description="Get a specific user by ID",
        responses={
            200: TUserSerializer,
            404: 'Not Found'
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific user by ID."""
        logger.info(f"Fetching user with ID: {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a user completely",
        request_body=TUserSerializer,
        responses={
            200: TUserSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    def update(self, request, *args, **kwargs):
        """Update a user completely."""
        logger.info(f"Updating user with ID: {kwargs.get('pk')}")
        try:
            response = super().update(request, *args, **kwargs)
            logger.info(f"User updated successfully: {response.data.get('username')}")
            return response
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise

    @swagger_auto_schema(
        operation_description="Update a user partially",
        request_body=TUserSerializer,
        responses={
            200: TUserSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """Update a user partially."""
        logger.info(f"Partially updating user with ID: {kwargs.get('pk')}")
        try:
            response = super().partial_update(request, *args, **kwargs)
            logger.info(f"User partially updated successfully: {response.data.get('username')}")
            return response
        except Exception as e:
            logger.error(f"Error partially updating user: {str(e)}")
            raise

    @swagger_auto_schema(
        operation_description="Delete a user",
        responses={
            204: 'No Content',
            404: 'Not Found'
        }
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a user."""
        user_id = kwargs.get('pk')
        logger.info(f"Deleting user with ID: {user_id}")
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info(f"User deleted successfully: {user_id}")
            return response
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            raise

    @swagger_auto_schema(
        operation_description="Get count of active users",
        responses={200: openapi.Response('Active user count', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'count': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ))}
    )
    @action(detail=False, methods=['get'])
    def active_count(self, request):
        """Get count of active users."""
        count = TUser.objects.filter(is_active=True).count()
        logger.info(f"Active user count: {count}")
        return Response({'count': count})
