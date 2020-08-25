from django.db import models
from django.contrib import auth  # has a lot of authorization tools
from posts.models import Post
# Create your models here.


class User(auth.models.User, auth.models.PermissionsMixin):


    # upvoted_posts = models.ManyToManyField(Post, related_name='users_who_upvoted')


    def __str__(self):
        return "@{}".format(self.username)  # username variable built into auth.models.user; documentation found here: https://docs.djangoproject.com/en/3.0/ref/contrib/auth/
  
