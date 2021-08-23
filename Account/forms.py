from django import forms
from django.contrib.auth.models import User

# Create your forms here.
class RegistrationUserForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.widgets.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.widgets.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')
