from django import forms
from .models import Client,Comments,ClientFile

class AddClientForm(forms.ModelForm):
    class Meta:
        model=Client
        fields=('name','email','description')


class AddCommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=('content',)


class AddFileForm(forms.ModelForm):
    class Meta:
        model=ClientFile
        fields=('file',)



