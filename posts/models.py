from django.db import models
from django.urls import reverse
import misaka
from cities.models import City, State
from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(
        User, related_name='posts',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now=True
    )
    title = models.CharField(
        max_length=100,
        null=True,
        # blank=True
    )
    message = models.TextField()
    message_html = models.TextField(
        editable=False
    )
    video = models.FileField(
        upload_to='videos/',
        null=True,
        blank=True
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        null=True,
        blank=True
    )
    location_information = models.CharField(
        max_length=120,
        null=True,
        blank=True
    )
    time_information = models.CharField(
        max_length=120,
        null=True,
        blank=True
    )
    state = models.ForeignKey(
        State,
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    city = models.ForeignKey(
        City,
        related_name='posts',
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    num_of_upvotes = models.IntegerField(
        default=0
    )
    num_of_downvotes = models.IntegerField(
        default=0
    )
    views = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # return reverse("posts:detail", kwargs={"username": self.user.username, "pk": self.pk})
        return reverse("posts:for_user", kwargs={"username": self.user.username})

    def total_upvotes(self):
        return self.upvotes.count()
    
    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_comments',
        blank=True,
        null=True
    )
    comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='comment_comments',
        blank=True,
        null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )
    message = models.TextField(
        max_length=200
    )
    created_at = models.DateTimeField(
        auto_now=True
    )
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "{} commented '{}'".format(self.user, self.message)


class Upvote(models.Model):
    user = models.ForeignKey(
        User,
        related_name='upvotes',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name='people_who_upvoted',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{} upvoted '{}'".format(self.user, self.post)


class Downvote(models.Model):
    user = models.ForeignKey(
        User,
        related_name='downvotes',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name='people_who_downvoted',
        on_delete=models.CASCADE
    )
    def __str__(self):
        return "{} downvoted '{}'".format(self.user, self.post)
