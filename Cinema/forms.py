from django import forms
from django.contrib.auth.models import User

from .models import Review, Film

class ReviewForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), to_field_name='id', required=False, widget=forms.HiddenInput())
    film = forms.ModelChoiceField(queryset=Film.objects.all(), to_field_name='id', required=False, widget=forms.HiddenInput())
    class Meta:
        model = Review
        fields = ('description', )
