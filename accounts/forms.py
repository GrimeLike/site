from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .apps import user_registered
from .models import User

class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class RegisteredUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адресс электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput)
    help_text = 'Введите тот же самый пароль ещё раз для проверки'

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1
    
    def clean(self):
        super().clean()
        password1 = self['password1']
        password2 = self['password2']
        if password1 and password2 != password2:
            errors = {'password2' : ValidationError ('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        user_registered.send(RegisteredUserForm, instance='user')
        return user
    
    class Meta:
        model = User
        fields =  ('username', 'email', 'password1', 'password2')

