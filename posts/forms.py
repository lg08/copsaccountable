from django import forms
from . import models

class PostForm(forms.ModelForm):
    class Meta:
        fields = ("message", "city")
        model = models.Post



    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["group"].queryset = (
                models.City.objects.filter(pk__in=user.groups.values_list("group__pk"))
            )


            # seems to be done rn
