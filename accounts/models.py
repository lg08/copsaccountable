from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
  




class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    # upvoted_posts = models.ManyToManyField(Post, related_name='users_who_upvoted')

    def __str__(self):
        return self.user.username


    # got this stuff from here: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()





class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)  # username variable built into auth.models.user; documentation found here: https://docs.djangoproject.com/en/3.0/ref/contrib/auth/
