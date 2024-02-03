from django import forms
from .models import Receita, ImagemReceita, Ingrediente
from django.forms import modelformset_factory

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['nome', 'instrucoes', 'ingredientes']
    
    ingredientes = forms.ModelMultipleChoiceField(
        queryset=Ingrediente.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

ImagemReceitaFormSet = modelformset_factory(
    ImagemReceita,
    fields=('imagem', ),
    extra=3, 
    max_num=5,
    widgets={'imagem': forms.FileInput(attrs={'class': 'form-control'})}
)
