from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from cities.models import City, State
from . import models
from . import views





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
    context_object_name = "cities_list"



class ListStates(generic.ListView):
    model = State
    template_name = "cities/states_list.html"
    context_object_name = "states_list"


class SingleState(generic.DetailView):
    model = State
    template_name = 'cities/state_detail.html'

