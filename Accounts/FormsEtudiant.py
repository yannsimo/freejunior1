from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from StudentApp.models import Student, School, Specialty, Program, Subject, SPECIALTY_CHOICES

User = get_user_model()



class UserForm(UserCreationForm):
    email = forms.EmailField(label="Adresse email", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Prénom", max_length=255, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Nom de famille", max_length=255, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class StudentRegistrationForm(forms.ModelForm):
    study_level = forms.ChoiceField(label="Niveau d’études", choices=Student.STUDY_LEVEL_CHOICES, required=True,
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    hourly_rate = forms.DecimalField(label="Taux horaire (€/heure)", required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        label="Brève description de vous-même",
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': (
                "Décrivez-vous brièvement. Voici quelques points à inclure pour atteindre les 100 mots : \n"
                "- Qui êtes-vous et quel est votre parcours académique ? \n"
                "- Quelles sont les stages que vous avez effectués ? \n"
                "- Sur quels projets avez-vous travaillé ? \n"
                "- Quelles compétences techniques maîtrisez-vous ? \n"
                "- Quelles sont vos compétences personnelles et vos forces ? \n"
                "- Quels sont vos objectifs professionnels ? \n"
                "- Quelles sont vos réalisations notables ? \n"
            )
        })
    )
    photo = forms.ImageField(label="Photo de profil", required=False,
                             widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    cv = forms.FileField(label="Curriculum Vitae (CV)", required=False,
                         widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    school_name = forms.CharField(label="Nom de l'école où vous étudiez", max_length=255, required=True,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de votre école'}))
    specialty_name = forms.ChoiceField(
        label="Spécialité que vous souhaitez exercer sur ce site ",
        choices=SPECIALTY_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    program_name = forms.CharField(label="Nom de votre filière universitaire", max_length=255, required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Entrez le nom de votre filière'}))
    subject_name = forms.CharField(label="Listez vos compétences ", max_length=255, required=True,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Listez vos compétences'}))

    class Meta:
        model = Student
        fields = ['study_level', 'hourly_rate', 'school_name', 'specialty_name', 'program_name', 'subject_name', 'description', 'photo','cv' ]

    def clean_description(self):
        description_text = self.cleaned_data.get('description')
        word_count = len(description_text.split())
        if word_count < 100:
            raise ValidationError('La description doit contenir au moins 100 mots.')
        return description_text

    def save(self, commit=True):
        school_name = self.cleaned_data.get('school_name')
        specialty_name = self.cleaned_data.get('specialty_name')
        program_name = self.cleaned_data.get('program_name')
        subject_name = self.cleaned_data.get('subject_name')

        with transaction.atomic():  # Commence une transaction atomique pour garantir l'intégrité des données
            # Crée ou récupère l'école, la spécialité, le programme et le sujet associés
            school, _ = School.objects.get_or_create(name=school_name)
            specialty, _ = Specialty.objects.get_or_create(name=specialty_name)
            program, _ = Program.objects.get_or_create(name=program_name, school=school)
            subject, _ = Subject.objects.get_or_create(name=subject_name, program=program)

            student = super().save(commit=False)
            student.school = school
            student.specialty = specialty
            student.program = program
            student.related_subject = subject

            if commit:
                student.save()  # Enregistre l'objet étudiant
        return student