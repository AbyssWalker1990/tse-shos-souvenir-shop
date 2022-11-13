from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
        )

        subject = 'Welcome for Souvenir Shop'
        message = 'Glad to see you with us'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()






post_save.connect(create_profile, sender=User)
post_delete.connect(delete_user, sender=Profile)
