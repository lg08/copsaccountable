from django import forms
from . import models
from .models import State, City
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class MyCustomPostFormView(forms.Form):
    state = forms.CharField()
    city = forms.CharField()
    title = forms.CharField()
    message = forms.CharField()
    video = forms.FileField(required=False)
    thumbnail = forms.ImageField(required=False)
    time_information = forms.CharField(required=False)
    location_information = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = super(MyCustomPostFormView, self).clean()
        if State.objects.filter(slug=slugify(cleaned_data['state'])):
            if City.objects.filter(state=State.objects.get(slug=slugify(cleaned_data['state'])), slug=slugify(cleaned_data['city'])):
                pass
            else:
                raise ValidationError(('Please check the spelling of the city'))
        else:
            raise ValidationError(('Please check the spelling of the state'))
        return cleaned_data
            

    # def clean_state(self):
    #     data = self.cleaned_data['state']
    #     if State.objects.filter(slug=slugify(data)):
    #         pass
    #     else:
    #         raise ValidationError(('Please check the spelling of the state'))
    #     return data
    
    # def clean_city(self):
    #     data = self.cleaned_data['city']
    #     if self.cleaned_data['state']:
    #         if City.objects.filter(slug=slugify(data), state=State.objects.get(slug=self.cleaned_data['state'])):
    #             pass
    #         else:
    #             raise ValidationError(('Sorry, we don\'t have that city on record. Please check our list of cities and report the missing city if necessary.'))
    #     else:
    #         raise ValidationError(('Please retype the state and try again.'))

    #     return data



# documentation can be here: https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
class PostForm(forms.ModelForm):
    # state = forms.ModelMultipleChoiceField(widget=)
    # city = forms.ModelMultipleChoiceField()
    
    class Meta:
        model = models.Post
        fields = (
            "title",
            "message",
            # "state",
            # "city",
            "time_information",
            "location_information",
            "video",
            "thumbnail"
                  )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

    
    # def save(self, commit=True):
    #     state = State.objects.get(slug=slugify(self.cleaned_data['state']))
    #     city = City.objects.get(slug=slugify(self.cleaned_data['city']))
    #     self.cleaned_data['state'] = state.id
    #     self.cleaned_data['city'] = city.id
    #     return super(PostForm, self).save(commit)



    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop("user", None)
    #     super().__init__(*args, **kwargs)
    #     if user is not None:
    #         self.fields["city"].queryset = (
    #             models.City.objects.filter(pk__in=user.cities.values_list("city__pk"))
    #         )


            # seems to be done rn


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('message', )



# class my_post_form_upload(forms.Form):
#     title = forms.CharField()
#     message = forms.CharField()
#     state = forms.CharField()
    
