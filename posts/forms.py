from django import forms
from . import models


# documentation can be here: https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ("title", "message", "city", "time_information", "location_information", "video", "thumbnail")



    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["city"].queryset = (
                models.City.objects.filter(pk__in=user.cities.values_list("city__pk"))
            )


            # seems to be done rn
