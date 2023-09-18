from django import forms
from .models import Concepts

class ConceptsForm(forms.ModelForm):
    class Meta:
        model = Concepts
        fields = ['title', 'definition', 'exampleText', 'exampleImg', 'source']
        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Cheetos',
                'required':'True',
                'autofocus':'True'
            }),

            'definition':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Los cheetos son...',
                'cols':'10',
                'rows':'5',
                'required':'True'
            }),

            'exampleText':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Hay varios tipos de cheetos...',
                'cols':'10',
                'rows':'3',
            }),


            'source':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'De los deseos',
            })
        }