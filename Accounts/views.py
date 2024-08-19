from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from Accounts.FormsEtudiant import UserRegistrationForm, StudentRegistrationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import login
from StudentApp.models import School, Specialty, Program, Subject
from Accounts.formseditionprofile import UserUpdateForm, StudentUpdateForm


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("page_etudiant")
            else:
                messages.error(request, "Identifiant ou mot de passe incorrect")
        else:
            messages.error(request, "Erreur de validation du formulaire")
    else:
        form = AuthenticationForm()
    return render(request, "Accounts/login.html", {"form": form})
def format_text_by_words(text, words_per_line=10):
    words = text.split()
    formatted_text = ""
    line = ""

    for i, word in enumerate(words):
        if i > 0 and i % words_per_line == 0:
            formatted_text += line.strip() + '\n'
            line = ""
        line += word + " "

    formatted_text += line.strip()
    return formatted_text


def logout_user(request):
    logout(request)
    return redirect("page_company")


@login_required
def edit_student_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        student_form = StudentUpdateForm(request.POST, request.FILES, instance=request.user.student)

        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès')
            return redirect('edit_student_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        student_form = StudentUpdateForm(instance=request.user.student)

    context = {
        'user_form': user_form,
        'student_form': student_form
    }
    return render(request, 'Accounts/edit_student_profile.html', context)

def register_student(request):
    step = request.POST.get('step', '1')

    if step == '1':
        user_form = UserRegistrationForm(request.POST or None)
        student_form = StudentRegistrationForm()

        if request.method == 'POST':
            if user_form.is_valid():
                # Store user data in session
                request.session['user_data'] = user_form.cleaned_data
                return render(request, 'Accounts/register_student_step1.html', {
                    'user_form': user_form,
                    'student_form': student_form,
                    'step': '2'
                })
            else:
                messages.error(request, "Erreur dans le formulaire utilisateur")
    else:
        # Retrieve user data from session
        user_data = request.session.get('user_data')
        user_form = UserRegistrationForm(user_data)
        student_form = StudentRegistrationForm(request.POST or None, request.FILES or None)

        if request.method == 'POST':
            if user_form.is_valid() and student_form.is_valid():
                with transaction.atomic():
                    user = user_form.save()
                    student = student_form.save(commit=False)
                    student.user = user

                    # Handle School
                    school_name = student_form.cleaned_data['school_name']
                    school = School.objects.filter(name=school_name).first()
                    if not school:
                        school = School.objects.create(name=school_name)

                    # Handle Specialty
                    specialty_name = student_form.cleaned_data['specialty_name']
                    specialty, _ = Specialty.objects.get_or_create(name=specialty_name)

                    # Handle Program
                    program_name = student_form.cleaned_data['program_name']
                    program, _ = Program.objects.get_or_create(name=program_name, school=school)

                    # Handle Subject
                    subject_name = student_form.cleaned_data['subject_name']
                    subject, _ = Subject.objects.get_or_create(name=subject_name, program=program)

                    # Set related fields
                    student.school = school
                    student.specialty = specialty
                    student.program = program
                    student.related_subject = subject

                    student.save()
                    login(request, user)
                    messages.success(request, 'Inscription réussie !')
                    return redirect('confirmationInscription')
            else:
                if not user_form.is_valid():
                    messages.error(request, "Erreur dans le formulaire utilisateur")
                if not student_form.is_valid():
                    messages.error(request, "Erreur dans le formulaire étudiant")

    return render(request, 'Accounts/register_student_step1.html', {
        'user_form': user_form,
        'student_form': student_form,
        'step': step
    })
import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
class SSORedirectView(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté

        # Créer le payload JWT
        payload = {
            'external_sso_id': str(user.id),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            # Ajoutez d'autres champs si nécessaire
        }

        # Générer le token JWT
        token = jwt.encode(payload, settings.SSO_SECRET_KEY, algorithm='HS256')

        # Mettre à jour les informations de connexion SSO
        user.update_sso_login()

        # Rediriger vers votre plateforme avec le token
        return redirect(f"{settings.YOUR_PLATFORM_SSO_URL}?token={token}")