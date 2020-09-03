from django.views.generic import TemplateView
from posts import models
from django.views.generic import ListView


class HomePage(ListView):
    template_name = 'index.html'
    model = models.Post
    select_related = ("user", "city")  # not entirely sure what this does yet


class AboutPage(TemplateView):
    template_name = 'about.html'


class TestPage(TemplateView):
    template_name = "test.html"


class ThanksPage(TemplateView):
    template_name = 'thanks.html'
