from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


# this model not in use rn but necessary to add fields later on
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    # got this stuff from here: https://simpleisbetterthancomplex.com/tutorial/
    # 2016/07/22/how-to-extend-django-user-model.html
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)
