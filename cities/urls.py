from django.urls import path
from . import views

app_name = 'cities'

urlpatterns = [
    path('cities/', views.ListCities.as_view(), name='all'),
    path("posts/in/<slug>/<int:pk>/",views.SingleCity.as_view(), name="single"),
    path('states/', views.ListStates.as_view(), name='list_states'), 
    path('cities/in/<slug>/', views.SingleState.as_view(), name='state_detail'),

    # path('create/all/states/', views.make_all_states, name='make_all_states'),
    path('create/cities/', views.make_all_the_cities, name='make_all_the_cities'),
]


# seems to be done
