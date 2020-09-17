import logging

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from banya.celeryapp import app


@app.task
def send_registration_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        url = reverse('core:home')
        from_email = f'"Банщик Интернет Магазин" <{settings.EMAIL_HOST_USER}>'
        subject = 'Банщик Интернет Магазин - Регистрация аккаунта.'
        html_message = render_to_string('store/email_customer_register.html',
                                        {'user': user, 'url': url})
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
