from django.urls import path
from . import views

app_name = 'cities'

urlpatterns = [
    path('', views.ListCities.as_view(), name = 'all'),
    path("posts/in/<slug>/",views.SingleCity.as_view(),name="single"),
]


# seems to be done
