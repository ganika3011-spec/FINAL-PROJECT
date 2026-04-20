from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)   
from .models import User, UserProfile

def detect_user_role(user):
    if user.is_authenticated:
        if user.Role == User.CUSTOMER:
            return 'customerdashboard'
        elif user.Role == User.RESTAURANT:
            return 'restaurantdashboard'
        elif user.is_superadmin:
            return 'admin:index'
    # Default redirect if no role or invalid role
    return 'customerdashboard'

def send_verification_email(request, user, mail_subject, email_template):
    """Send account verification email. Handles email errors gracefully."""
    try:
        current_site = get_current_site(request)
        message = render_to_string(email_template, {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            subject=mail_subject, 
            body=message, 
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        email.content_subtype = 'html'  # Set email as HTML
        email.send()
        logger.info(f"Verification email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
        # Don't crash the registration process if email fails
        # In production, you might want to handle this differently    

def send_notification(mail_subject, mail_template, context):
    """Send notification email. Handles email errors gracefully."""
    try:
        
        message = render_to_string(mail_template, context)
        to_email = context.get('user').email
        email = EmailMessage(
            subject=mail_subject, 
            body=message, 
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        email.content_subtype = 'html'  # Set email as HTML
        email.send()
        logger.info(f"Notification email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send notification email to {context.get('user').email}: {str(e)}")
        # Don't crash the process if email fails
        # In production, you might want to handle this differently  