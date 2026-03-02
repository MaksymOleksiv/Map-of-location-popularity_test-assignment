from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            instance.request.build_absolute_uri(
                reverse("password_reset:reset-password-confirm")
            ),
            reset_password_token.key,
        ),
    }

    email_html_message = "Hello {username}, here is your password reset token: {token}.\nOr use this link: {url}".format(
        username=reset_password_token.user.username,
        token=reset_password_token.key,
        url=context["reset_password_url"],
    )

    msg = EmailMultiAlternatives(
        "Password Reset for {title}".format(title="Map Location App"),
        email_html_message,
        "test@example.local",
        [reset_password_token.user.email],
    )
    msg.send()
