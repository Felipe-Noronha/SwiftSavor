from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import ImagemReceita, Receita, Ingrediente, UsuarioIngrediente
from django.forms import modelformset_factory

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


class UsuarioIngredienteForm(forms.ModelForm):
    class Meta:
        model = UsuarioIngrediente
        fields = ['ingrediente', 'quantidade']

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields['ingrediente'].queryset = Ingrediente.objects.exclude(
                id__in=UsuarioIngrediente.objects.filter(usuario=usuario).values_list('ingrediente_id', flat=True)
            )


ImagemReceitaFormSet = modelformset_factory(
    ImagemReceita,
    fields=('imagem', ),
    extra=3,
    max_num=5
)