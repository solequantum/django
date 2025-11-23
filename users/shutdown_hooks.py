"""
Shutdown Hooks for Django Application.

This module provides Java-style shutdown hook functionality for Django.
It ensures proper cleanup of resources (database connections, caches, etc.)
when the application shuts down.

Usage:
    Hooks are automatically registered when the app starts.
    They execute when the Python interpreter exits.
"""

import atexit
import logging
import signal
import sys
from django.db import connections

logger = logging.getLogger(__name__)


class ShutdownHookManager:
    """
    Manages shutdown hooks similar to Java's Runtime.addShutdownHook().

    This class provides:
    - Registration of cleanup functions
    - Graceful shutdown on SIGTERM/SIGINT signals
    - Automatic database connection cleanup
    - Custom hook registration for application-specific cleanup
    """

    _instance = None
    _hooks = []
    _is_shutting_down = False

    def __new__(cls):
        """Singleton pattern to ensure only one manager exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the shutdown hook manager."""
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._register_default_hooks()
            self._register_signal_handlers()

    def _register_default_hooks(self):
        """Register default cleanup hooks."""
        # Register the main cleanup function with atexit
        atexit.register(self._execute_hooks)
        logger.info("Shutdown hook manager initialized")

    def _register_signal_handlers(self):
        """Register signal handlers for graceful shutdown."""
        # Handle SIGTERM (kill command) and SIGINT (Ctrl+C)
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        logger.debug("Signal handlers registered for SIGTERM and SIGINT")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        signal_name = signal.Signals(signum).name
        logger.info(f"Received {signal_name} signal, initiating graceful shutdown...")
        self._execute_hooks()
        sys.exit(0)

    def register_hook(self, hook_func, name=None, priority=10):
        """
        Register a custom shutdown hook.

        Args:
            hook_func: Callable to execute during shutdown
            name: Optional name for logging purposes
            priority: Lower numbers execute first (default: 10)

        Example:
            def my_cleanup():
                print("Cleaning up my resources...")

            ShutdownHookManager().register_hook(my_cleanup, name="MyCleanup")
        """
        hook_name = name or hook_func.__name__
        self._hooks.append({
            'func': hook_func,
            'name': hook_name,
            'priority': priority
        })
        # Sort by priority (lower first)
        self._hooks.sort(key=lambda x: x['priority'])
        logger.debug(f"Registered shutdown hook: {hook_name} (priority: {priority})")

    def _execute_hooks(self):
        """Execute all registered shutdown hooks."""
        if self._is_shutting_down:
            return  # Prevent double execution

        self._is_shutting_down = True
        logger.info("=" * 50)
        logger.info("SHUTDOWN INITIATED - Executing cleanup hooks...")
        logger.info("=" * 50)

        # Execute custom hooks first
        for hook in self._hooks:
            try:
                logger.info(f"Executing hook: {hook['name']}")
                hook['func']()
                logger.info(f"Hook completed: {hook['name']}")
            except Exception as e:
                logger.error(f"Error in hook {hook['name']}: {str(e)}")

        # Always cleanup database connections last
        self._cleanup_database_connections()

        logger.info("=" * 50)
        logger.info("SHUTDOWN COMPLETE - All resources released")
        logger.info("=" * 50)

    def _cleanup_database_connections(self):
        """Close all database connections and dispose connection pools."""
        logger.info("Closing database connections...")

        try:
            # Close all Django database connections
            for alias in connections:
                connection = connections[alias]
                try:
                    # Close the connection
                    connection.close()
                    logger.info(f"Closed database connection: {alias}")

                    # If using connection pool, dispose of it
                    if hasattr(connection, 'pool') and connection.pool:
                        connection.pool.dispose()
                        logger.info(f"Disposed connection pool for: {alias}")

                except Exception as e:
                    logger.error(f"Error closing connection {alias}: {str(e)}")

            # Additional cleanup for SQLAlchemy pools (used by django-db-connection-pool)
            self._cleanup_sqlalchemy_pools()

        except Exception as e:
            logger.error(f"Error during database cleanup: {str(e)}")

    def _cleanup_sqlalchemy_pools(self):
        """Cleanup SQLAlchemy connection pools if present."""
        try:
            from sqlalchemy import event
            from sqlalchemy.pool import Pool

            # Dispose all pools
            Pool.dispose()
            logger.info("SQLAlchemy connection pools disposed")
        except ImportError:
            pass  # SQLAlchemy not installed
        except Exception as e:
            logger.debug(f"SQLAlchemy pool cleanup: {str(e)}")


# =============================================================================
# Convenience Functions
# =============================================================================

def register_shutdown_hook(func, name=None, priority=10):
    """
    Convenience function to register a shutdown hook.

    Args:
        func: Function to call during shutdown
        name: Optional name for the hook
        priority: Execution priority (lower = earlier, default: 10)

    Example:
        @register_shutdown_hook
        def cleanup_temp_files():
            # cleanup logic here
            pass

        # Or with parameters:
        register_shutdown_hook(my_cleanup_func, name="MyCleanup", priority=5)
    """
    manager = ShutdownHookManager()
    manager.register_hook(func, name, priority)
    return func


def get_shutdown_manager():
    """Get the singleton ShutdownHookManager instance."""
    return ShutdownHookManager()


# =============================================================================
# Default Hooks (can be customized)
# =============================================================================

def cleanup_celery_workers():
    """Cleanup Celery workers if running."""
    try:
        from user_management.celery import app as celery_app
        celery_app.control.shutdown()
        logger.info("Celery workers shutdown signal sent")
    except Exception as e:
        logger.debug(f"Celery cleanup: {str(e)}")


def cleanup_cache_connections():
    """Close cache connections."""
    try:
        from django.core.cache import caches
        for cache_name in caches:
            try:
                caches[cache_name].close()
                logger.info(f"Closed cache connection: {cache_name}")
            except Exception:
                pass
    except Exception as e:
        logger.debug(f"Cache cleanup: {str(e)}")


def log_shutdown_statistics():
    """Log shutdown statistics."""
    import datetime
    logger.info(f"Shutdown time: {datetime.datetime.now().isoformat()}")
