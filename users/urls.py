"""
URL configuration for users app.
Defines the REST API endpoints for user CRUD operations.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TUserViewSet

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'', TUserViewSet, basename='tuser')

urlpatterns = [
    path('', include(router.urls)),
]
