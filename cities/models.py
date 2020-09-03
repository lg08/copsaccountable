from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()


class State(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )
    slug = models.SlugField(
        allow_unicode=True,
        unique=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("cities:state_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["name"]


class City(models.Model):
    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        allow_unicode=True
    )
    state = models.ForeignKey(
        State,
        related_name="cities",
        on_delete=models.CASCADE,
        default=1)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("cities:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["name"]
