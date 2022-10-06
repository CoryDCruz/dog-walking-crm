from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Activity
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ('date', 'activity')

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])

    class Meta: 
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')
