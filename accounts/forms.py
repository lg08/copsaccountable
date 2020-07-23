from django.contrib.auth import get_user_model  # returns the user model that is currently active in this project
from django.contrib.auth.forms import UserCreationForm  # basically generates the usercreation form for us; check the documentation


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')  # these are the fiels we want the user to fill out
        model = get_user_model                                    # allows us to get the model of whoever's accessing the website


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Public Display Name"  # this just sets the label for the fields on the form
        self.fields['email'].label = "Email Address"
