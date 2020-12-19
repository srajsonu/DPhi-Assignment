from django import forms
from django.contrib.auth.models import User

from user.models import Plants


class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class PlantsForm(forms.ModelForm):
    class Meta:
        model = Plants
        exclude = ['manager']
