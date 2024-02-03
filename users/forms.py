from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User



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
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'id': 'old_password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'id': 'new_password1'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'id': 'new_password2'})