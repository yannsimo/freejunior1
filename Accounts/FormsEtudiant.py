from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from StudentApp.models import Student, School, Specialty, Program, Subject, SPECIALTY_CHOICES
from django.core.validators import URLValidator
from pydantic import ValidationError

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Adresse email",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nom@exemple.com'})
    )
    first_name = forms.CharField(
        label="Prénom",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre prénom'})
    )
    last_name = forms.CharField(
        label="Nom de famille",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom de famille'})
    )
    password1 = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre mot de passe'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class StudentRegistrationForm(forms.ModelForm):
    study_level = forms.ChoiceField(
        label="Niveau d'études", choices=Student.STUDY_LEVEL_CHOICES, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    hourly_rate = forms.DecimalField(
        label="Taux horaire (€/heure)", required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label="Brève description de vous-même",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Décrivez-vous brièvement."})
    )
    photo = forms.ImageField(
        label="Photo de profil", required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
    cv = forms.FileField(
        label="Curriculum Vitae (CV)", required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
    school_name = forms.CharField(
        label="Nom de l'école où vous étudiez", max_length=255, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    specialty_name = forms.ChoiceField(
        label="Spécialité que vous souhaitez exercer sur ce site",
        choices=SPECIALTY_CHOICES, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    program_name = forms.CharField(
        label="Nom de votre filière universitaire", max_length=255, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    subject_name = forms.CharField(
        label="Listez vos compétences", max_length=255, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    portfolio_url = forms.URLField(
        label="URL du portfolio", required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = ['study_level', 'hourly_rate', 'school_name', 'specialty_name', 'program_name', 'subject_name', 'description', 'photo', 'cv', 'portfolio_url']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("La taille de l'image ne doit pas dépasser 5MB.")
            if not photo.content_type.startswith('image'):
                raise forms.ValidationError("Le fichier doit être une image.")
        return photo

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Les mots de passe ne correspondent pas.")

    def clean_portfolio_url(self):
        url = self.cleaned_data.get('portfolio_url')
        if url:
            try:
                URLValidator()(url)
            except ValidationError:
                raise forms.ValidationError("Veuillez entrer une URL valide.")
        return url