from django import forms
from .models import Ingrediente, UsuarioIngrediente

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nome']

    def clean_nome(self):
        nome = self.cleaned_data['nome'].lower()
    
        if Ingrediente.objects.filter(nome__iexact=nome).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Um ingrediente com esse nome já existe.')

        return nome    

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

