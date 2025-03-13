from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django_channels_chat import settings


def send_verify_mail(request, user):
    subject = 'Verify your account'
    email_template_name = "registration/password_verify_email.html"
    email = user.email
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain
    token_generator = PasswordResetTokenGenerator()

    context = {
        "email": user.email,
        "domain": domain,
        "site_name": site_name,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        "token": token_generator.make_token(user),
        "protocol": "http",

    }
    message = loader.render_to_string(email_template_name, context)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(
        subject,
        message,
        from_email,
        recipient_list)
