from django import forms
from .models import Company, User

class EntrepriseForm(forms.ModelForm):
    email = forms.EmailField(label="Adresse email")
    first_name = forms.CharField(label="Prénom", max_length=30)
    last_name = forms.CharField(label="Nom", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Company
        fields = ['name', 'contact_info']

    def save(self, commit=True):
        # Créer ou mettre à jour l'utilisateur
        user_data = {
            'email': self.cleaned_data['email'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'user_type': 'COMPANY'
        }
        user, created = User.objects.update_or_create(
            email=user_data['email'],
            defaults=user_data
        )
        if created:
            user.set_password(self.cleaned_data['password'])
        user.save()

        # Créer ou mettre à jour l'entreprise
        company = super().save(commit=False)
        company.user = user
        if commit:
            company.save()
        return company