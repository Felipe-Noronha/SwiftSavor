from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
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


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(
        label='Novo E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
    )

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'    