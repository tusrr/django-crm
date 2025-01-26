from django import forms
from .models import Lead,Comments

class AddLeadForm(forms.ModelForm):
    class Meta:
        model=Lead
        fields=('name','email','description','priority', 'status',)

class AddCommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=('content',)

