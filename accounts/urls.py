from django.urls import path
from django.contrib.auth import views as auth_views  # automatically generates login and logout views
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name = 'accounts/login.html'), name ='login'),  # this uses the automatically created loginView from auth_views and passes it to the template we made
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),  # using the template view for this one, so we don't need to pass in a template
    path('signup/', views.SignUp.as_view(), name = 'signup'),
]
