from django import forms
from django.contrib.auth.models import User

from PersonalCabinet.models import UserPrivacy


class UserPrivacyForm(forms.ModelForm):
    isPrivacy = forms.BooleanField(label="Приватный список:", required=False)

    class Meta:
        model = UserPrivacy
        fields = ('isPrivacy', )
