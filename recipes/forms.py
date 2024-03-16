from django import forms
from .models import Receita, ImagemReceita, Ingrediente
from django.forms import modelformset_factory

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['nome', 'instruções', 'ingredientes']
    
    ingredientes = forms.ModelMultipleChoiceField(
        queryset=Ingrediente.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

ImagemReceitaFormSet = modelformset_factory(
    ImagemReceita,
    fields=('imagem','url'),
    extra=3, 
    max_num=5,
    widgets={
        'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        'url': forms.URLInput(attrs={'class': 'form-control'}),
        }
)

class PesquisaReceitaForm(forms.Form):
    pesquisa = forms.CharField(max_length=100, required=False, label='Pesquisar')


class EditarReceitaForm(forms.ModelForm):
    ingredientes = forms.ModelMultipleChoiceField(
        queryset=Ingrediente.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Receita
        fields = ['nome', 'instruções', 'ingredientes']

class EditarImagemReceitaForm(forms.ModelForm):
    class Meta:
        model = ImagemReceita
        fields = ['imagem', 'url']