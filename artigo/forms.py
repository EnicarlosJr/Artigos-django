# artigos/forms.py
from django import forms
from .models import Artigo

class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = "__all__"

class ConfirmacaoExclusaoForm(forms.Form):
    confirmar = forms.BooleanField(label='Confirmar exclusão?')
