from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Company, Mission, PAYMENT_CHOICES, SPECIALTY_CHOICES, Specialty

class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email', 'contact_info']
        labels = {
            'name': "Entrez le nom de l'entreprise",
            'email': "Entrez l'adresse email de l'entreprise",
            'contact_info': "Entrez le numéro de téléphone de l'entreprise",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Company.objects.filter(email=email).exists():
            raise ValidationError("Une entreprise avec cet email existe déjà.")
        return email

    def clean_contact_info(self):
        contact_info = self.cleaned_data.get('contact_info')
        if not contact_info.isdigit():
            raise ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")
        return contact_info

class MissionForm(forms.ModelForm):
    title = forms.CharField(
        label="Ecrire le titre de la mission",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ecrire le titre de la mission'})
    )
    description = forms.CharField(
        label="Brève description de la mission",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Décrivez brièvement la mission'})
    )
    payment_type = forms.ChoiceField(
        label="Type de paiement",
        choices=PAYMENT_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_payment_type'})
    )
    specialty_name = forms.ChoiceField(
        label="Type de Mission",
        choices=SPECIALTY_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Mission
        fields = ['title', 'specialty_name', 'description', 'payment_type']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
        }


    def save(self, commit=True):
        specialty_name = self.cleaned_data.get('specialty_name')
        with transaction.atomic():
            specialty, created = Specialty.objects.get_or_create(name=specialty_name)
            mission = super().save(commit=False)
            mission.specialty = specialty
            if commit:
                mission.save()
        return mission