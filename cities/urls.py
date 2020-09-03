from django.urls import path
from . import views

app_name = 'cities'

urlpatterns = [
    # lists all the states in the country
    path(
        'states/',
        views.ListStates.as_view(),
        name='list_states'
    ),
    # lists all the cities in a state
    path(
        'cities/in/<slug>/',
        views.SingleState.as_view(),
        name='state_detail'
    ),
    # lists all the posts in the city
    path(
        "posts/in/<slug>/<int:pk>/",
        views.SingleCity.as_view(),
        name="single"
    ),
    # be careful with this guy
    # path(
    #     'create/cities/',
    #     views.make_all_the_cities,
    #     name='make_all_the_cities'
    # ),
]
