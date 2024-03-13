from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1 is None:
            raise ValidationError("A senha não pode ser nula.")

        if len(password1) < 8:
            raise ValidationError("A senha deve ter pelo menos 8 caracteres.")

        if not any(char.isupper() for char in password1):
            raise ValidationError("A senha deve conter pelo menos uma letra maiúscula.")

        special_characters = "!@#$%^&*()_-+=<>?/[]{}|"
        if not any(char in special_characters for char in password1):
            raise ValidationError("A senha deve conter pelo menos um caractere especial.")

        common_passwords = ['password', '123456', 'qwerty', 'abc123']
        if password1.lower() in common_passwords:
            raise ValidationError("A senha não pode ser uma senha comum.")

        return password1


class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(
        label='Novo E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
    )


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'id': 'old_password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'id': 'new_password1'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'id': 'new_password2'})