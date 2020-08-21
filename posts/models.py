from django.db import models
from django.conf import settings
from django.urls import reverse

import misaka

from cities.models import City

from django.contrib.auth import get_user_model
User = get_user_model()



class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)  # maybe change this later
    created_at = models.DateTimeField(auto_now=True)

    # I'm testing this out
    title = models.TextField(max_length=50, default='post_title')
    
    message = models.TextField()
    message_html = models.TextField(editable=False)
    city = models.ForeignKey(City, related_name='posts', null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("posts:single", kwargs={"username": self.user.username, "pk": self.pk})

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]



        # seems to be done rn, but doesn't have videos rn


        
