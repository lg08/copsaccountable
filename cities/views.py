from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from cities.models import City
from . import models





# documentation can be found here: https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-display/

# I think this automatically searches for template names if none are defined, but you can also define a "template_name"
class SingleCity(generic.DetailView):
    model = City
    template_name = "cities/cities_detail.html"


    # doc here: https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-display/
class ListCities(generic.ListView):
    model = City
    template_name = "cities/cities_list.html"
    # good choice for template name is something like "cities_list.html"

    #  seems to be done
