from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from StudentApp.models import Student, SPECIALTY_CHOICES
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from StudentApp.models import Specialty, School, Program, Subject

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

class StudentRegistrationForm(UserRegistrationForm):
    study_level = forms.ChoiceField(
        label="Niveau d'études", choices=Student.STUDY_LEVEL_CHOICES, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    specialty = forms.ModelChoiceField(
        queryset=Specialty.objects.all(),
        label="Spécialité",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        label="École",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    program = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        label="Programme",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    related_subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label="Matière associée",
        required=True,
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
    portfolio_url = forms.URLField(
        label="URL du portfolio", required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
        )

    class Meta(UserRegistrationForm.Meta):
        fields = UserRegistrationForm.Meta.fields + [
            'study_level', 'specialty', 'school', 'program', 'related_subject',
            'hourly_rate', 'description', 'photo', 'cv', 'portfolio_url'
            ]

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

    def clean_portfolio_url(self):
        url = self.cleaned_data.get('portfolio_url')
        if url:
            try:
                URLValidator()(url)
            except ValidationError:
                raise forms.ValidationError("Veuillez entrer une URL valide.")
        return url

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'STUDENT'
        if commit:
            user.save()
            student = Student.objects.create(
                user=user,
                study_level=self.cleaned_data['study_level'],
                specialty=self.cleaned_data['specialty'],
                school=self.cleaned_data['school'],
                program=self.cleaned_data['program'],
                related_subject=self.cleaned_data['related_subject'],
                hourly_rate=self.cleaned_data['hourly_rate'],
                description=self.cleaned_data['description'],
                photo=self.cleaned_data['photo'],
                cv=self.cleaned_data['cv'],
                portfolio_url=self.cleaned_data['portfolio_url']
            )
        return user