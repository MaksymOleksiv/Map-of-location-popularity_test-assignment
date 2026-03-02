from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Review, Subscription


@receiver(post_save, sender=Review)
def send_notification_on_new_review(sender, instance, created, **kwargs):
    if created:
        review = instance
        location = review.location

        subscribers = Subscription.objects.filter(location=location).exclude(
            user=review.user
        )

        if not subscribers.exists():
            return

        recipient_list = [sub.user.email for sub in subscribers if sub.user.email]

        if not recipient_list:
            return

        subject = f'New Review for "{location.title}"'
        message = (
            f"Hello!\n\n"
            f"A new review was added to the location '{location.title}' by {review.user.username}.\n\n"
            f"Review:\n{review.text}\n\n"
            f"Map Location App Team"
        )

        send_mail(
            subject,
            message,
            (
                settings.DEFAULT_FROM_EMAIL
                if hasattr(settings, "DEFAULT_FROM_EMAIL")
                else "test@example.local"
            ),
            recipient_list,
            fail_silently=False,
        )
