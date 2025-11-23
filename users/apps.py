"""
Users app configuration.

This module configures the users app and initializes shutdown hooks
for proper resource cleanup when the application terminates.
"""

from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class UsersConfig(AppConfig):
    """
    Configuration for the users application.

    This AppConfig:
    - Sets up the default auto field for models
    - Initializes shutdown hooks for graceful resource cleanup
    - Registers custom cleanup functions (similar to Java shutdown hooks)
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'User Management'

    def ready(self):
        """
        Called when Django starts.

        This method initializes:
        - Shutdown hook manager for graceful cleanup
        - Signal handlers for SIGTERM/SIGINT
        - Custom cleanup hooks for application resources
        """
        # Only run in the main process (not in management commands or migrations)
        import sys
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0] if sys.argv else False:
            self._initialize_shutdown_hooks()

    def _initialize_shutdown_hooks(self):
        """Initialize shutdown hooks for resource cleanup."""
        try:
            from .shutdown_hooks import (
                ShutdownHookManager,
                cleanup_celery_workers,
                cleanup_cache_connections,
                log_shutdown_statistics
            )

            # Get the shutdown manager (singleton)
            manager = ShutdownHookManager()

            # Register default cleanup hooks with priorities
            # Lower priority = executes first
            manager.register_hook(log_shutdown_statistics, "LogStatistics", priority=1)
            manager.register_hook(cleanup_cache_connections, "CacheCleanup", priority=5)
            manager.register_hook(cleanup_celery_workers, "CeleryCleanup", priority=8)

            # Database connections are always cleaned up last (built into manager)

            logger.info("Shutdown hooks initialized successfully")

        except Exception as e:
            logger.warning(f"Could not initialize shutdown hooks: {str(e)}")
