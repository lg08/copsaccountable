from django import forms
from .models import Comment
from cities.models import City, State
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class PostForm(forms.Form):
    title = forms.CharField()
    message = forms.CharField()
    state = forms.CharField()
    city = forms.CharField()
    video = forms.FileField(required=False)
    thumbnail = forms.ImageField(required=False)
    time_information = forms.CharField(required=False)
    location_information = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        if State.objects.filter(slug=slugify(cleaned_data['state'])):
            if City.objects.filter(
                    state=State.objects.get(
                        slug=slugify(cleaned_data['state'])),
                    slug=slugify(cleaned_data['city'])):
                pass
            else:
                raise ValidationError('Please check the spelling of the city')
        else:
            raise ValidationError('Please check the spelling of the state')
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message', )
