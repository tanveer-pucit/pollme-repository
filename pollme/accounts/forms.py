from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        label='username',
        max_length=50,
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(
        label='password',
        max_length=50,
        min_length=3,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='confirm password',
        max_length=50,
        min_length=3,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError('Email is already register!')
        return email

    # def clean_password1(self):
    #     # This raises error because it called the moment u entered password1 but that time password2 does not exists
    #     p1 = self.cleaned_data['password1']
    #     p2 = self.cleaned_data['password2']
    #     if p1 != p2:
    #         raise ValidationError('Password not same enter again!')
    #     return p1

    # def clean_password2(self):
    #     p1 = self.cleaned_data['password1']
    #     p2 = self.cleaned_data['password2']
    #     if p1 != p2:
    #         raise ValidationError('Password not same enter again!')
    #     return p2

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 and p2:
            if p1 != p2:
                raise ValidationError('Password not same enter again!')
