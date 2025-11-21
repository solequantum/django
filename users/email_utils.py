"""
Email utilities for the users app.
Provides functions to send various types of emails.
"""
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_user_welcome_email(user_email, username):
    """
    Send a welcome email to a new user.

    Args:
        user_email: The email address of the user
        username: The username of the user

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    subject = 'Welcome to User Management System'
    message = f"""
    Hello {username},

    Welcome to the User Management System!

    Your account has been successfully created.

    Best regards,
    User Management Team
    """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info(f"Welcome email sent to {user_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user_email}: {str(e)}")
        return False


def send_user_notification_email(user_email, username, notification_message):
    """
    Send a notification email to a user.

    Args:
        user_email: The email address of the user
        username: The username of the user
        notification_message: The notification message to send

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    subject = 'User Management System Notification'
    message = f"""
    Hello {username},

    {notification_message}

    Best regards,
    User Management Team
    """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info(f"Notification email sent to {user_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send notification email to {user_email}: {str(e)}")
        return False


def send_bulk_email(subject, message, recipient_list):
    """
    Send bulk email to multiple recipients.

    Args:
        subject: Email subject
        message: Email message
        recipient_list: List of email addresses

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info(f"Bulk email sent to {len(recipient_list)} recipients")
        return True
    except Exception as e:
        logger.error(f"Failed to send bulk email: {str(e)}")
        return False


def send_html_email(subject, html_content, recipient_list):
    """
    Send HTML email.

    Args:
        subject: Email subject
        html_content: HTML content of the email
        recipient_list: List of email addresses

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
        )
        email.content_subtype = 'html'
        email.send()
        logger.info(f"HTML email sent to {len(recipient_list)} recipients")
        return True
    except Exception as e:
        logger.error(f"Failed to send HTML email: {str(e)}")
        return False
