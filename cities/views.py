from django.views import generic
from cities.models import City, State


# lists all states
class ListStates(generic.ListView):
    model = State
    template_name = "cities/states_list.html"
    context_object_name = "states_list"


# lists all the cities in a state
class SingleState(generic.DetailView):
    model = State
    template_name = 'cities/state_detail.html'


# lists all the posts in a city
class SingleCity(generic.DetailView):
    model = City
    template_name = "cities/cities_detail.html"
