from django import forms
from .models import Receita
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['nome', 'ingredientes', 'instrucoes']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']