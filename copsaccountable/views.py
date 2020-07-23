from django.views.generic import TemplateView

class HomePage(TemplateView):
    template_name = 'index.html'



class AboutPage(TemplateView):
    template_name = 'about.html'
