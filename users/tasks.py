"""
Celery tasks for the users app.
Provides scheduled tasks and asynchronous operations.
"""
from celery import shared_task
from django.utils import timezone
from .models import TUser
from .email_utils import send_bulk_email
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email_task(user_id):
    """
    Asynchronous task to send welcome email to a new user.

    Args:
        user_id: The ID of the user

    Returns:
        str: Status message
    """
    try:
        from .email_utils import send_user_welcome_email
        user = TUser.objects.get(id=user_id)
        send_user_welcome_email(user.email, user.username)
        logger.info(f"Welcome email task completed for user {user.username}")
        return f"Welcome email sent to {user.email}"
    except TUser.DoesNotExist:
        logger.error(f"User with ID {user_id} not found")
        return f"User with ID {user_id} not found"
    except Exception as e:
        logger.error(f"Error in send_welcome_email_task: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def cleanup_inactive_users():
    """
    Scheduled task to cleanup or report inactive users.
    This can be scheduled using Celery Beat.

    Returns:
        str: Status message
    """
    try:
        inactive_users = TUser.objects.filter(is_active=False)
        count = inactive_users.count()
        logger.info(f"Found {count} inactive users")

        # You can add logic here to delete or notify about inactive users
        # For example, delete users inactive for more than 90 days

        return f"Processed {count} inactive users"
    except Exception as e:
        logger.error(f"Error in cleanup_inactive_users task: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def generate_daily_report():
    """
    Scheduled task to generate daily user statistics report.
    This can be scheduled using Celery Beat.

    Returns:
        str: Status message
    """
    try:
        total_users = TUser.objects.count()
        active_users = TUser.objects.filter(is_active=True).count()
        inactive_users = TUser.objects.filter(is_active=False).count()

        today = timezone.now().date()
        new_users_today = TUser.objects.filter(created_at__date=today).count()

        report = f"""
        Daily User Report - {today}
        ===========================
        Total Users: {total_users}
        Active Users: {active_users}
        Inactive Users: {inactive_users}
        New Users Today: {new_users_today}
        """

        logger.info(f"Daily report generated: {report}")
        return report
    except Exception as e:
        logger.error(f"Error in generate_daily_report task: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def send_bulk_notification(subject, message, user_filter=None):
    """
    Asynchronous task to send bulk notifications to users.

    Args:
        subject: Email subject
        message: Email message
        user_filter: Optional filter dict for users (e.g., {'is_active': True})

    Returns:
        str: Status message
    """
    try:
        if user_filter:
            users = TUser.objects.filter(**user_filter)
        else:
            users = TUser.objects.all()

        recipient_list = [user.email for user in users if user.email]

        if recipient_list:
            send_bulk_email(subject, message, recipient_list)
            logger.info(f"Bulk notification sent to {len(recipient_list)} users")
            return f"Notification sent to {len(recipient_list)} users"
        else:
            logger.warning("No users found for bulk notification")
            return "No users found"
    except Exception as e:
        logger.error(f"Error in send_bulk_notification task: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def scheduled_backup_reminder():
    """
    Example scheduled task that can run periodically.
    This demonstrates the scheduling capability similar to Quartz in Java.

    Returns:
        str: Status message
    """
    try:
        logger.info("Scheduled backup reminder task executed")
        # Add your scheduled task logic here
        return "Backup reminder task completed"
    except Exception as e:
        logger.error(f"Error in scheduled_backup_reminder task: {str(e)}")
        return f"Error: {str(e)}"
