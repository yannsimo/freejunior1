from django import forms
from .models import Comment

class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['company_name','mission_title','text']
        labels = {
            'company_name': 'Nom de la compagnie',
            'mission_title': 'Titre de la mission',
            'text': 'Entrez votre commentaire'
        }