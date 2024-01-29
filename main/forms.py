from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Receita, Ingrediente

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['nome', 'instrucoes','ingredientes']

    ingredientes = forms.ModelMultipleChoiceField(
        queryset=Ingrediente.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nome']        