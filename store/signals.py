from django.conf import settings

from store.tasks import send_registration_email


def user_post_save(sender, instance, created, *args, **kwargs):
    if settings.DEBUG:
        return
    if created:
        send_registration_email.delay(instance.pk)
