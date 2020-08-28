# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms

# Create your views here.


# see docimentation here: https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/
class SignUp(CreateView):
    form_class = forms.UserCreateForm  # this is just setting them equal to each other, no instantiating
    success_url = reverse_lazy('login')  # on a successful sign up, they will be redirected to login page
    template_name = 'accounts/signup.html'
