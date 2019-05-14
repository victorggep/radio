from django import forms

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