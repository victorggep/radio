from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Noticia


class NoticiaForm(forms.ModelForm):

    class Meta:
        model = Noticia
        fields = ['titular', 'resum', 'cos_noticia']

        widgets = {
            'titular': forms.TextInput(attrs={"class": "form-control"}),
            'resum': forms.Textarea(attrs={"class": "form-control"}),
            'cos_noticia': forms.Textarea(attrs={"class": "form-control"})
        }


class RegistrarUsuariForm(forms.Form):
    username = forms.CharField(label="Nom d'usuari", min_length=4, max_length=150, widget=forms.TextInput)
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Contrasenya', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma contrasenya', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Ja existeix aquest usuari")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Ja exiteix aquest email")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Les contrasenyes no coincideixen")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class CanviContrasenyaForm(forms.Form):
    password_antic = forms.CharField(label='Antiga contrasenya', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Contrasenya', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeteix Contrasenya', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Les contrasenyes no coincideixen")

        return password2