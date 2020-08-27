from django.urls import path
from . import views

app_name = 'cities'

urlpatterns = [
    path('cities/', views.ListCities.as_view(), name='all'),
    path("posts/in/<slug>/",views.SingleCity.as_view(), name="single"),
    path('states/', views.ListStates.as_view(), name='list_states'), 
    path('cities/in/<slug>/', views.SingleState.as_view(), name='state_detail'),

    path('create/all/cities/', views.make_all_states, name='make_all_states'),
]


# seems to be done
