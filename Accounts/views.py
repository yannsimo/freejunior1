from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from Accounts.FormsEtudiant import UserForm, StudentRegistrationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

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

def register_student(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():
            try:
                user = user_form.save()
                user.save()
                student = student_form.save(commit=False)
                student.user = user  # Relier l'utilisateur et l'étudiant

                # Reformater le texte des compétences avant de sauvegarder
                student.subject_name = format_text_by_words(student.subject_name, words_per_line=10)

                student.save()

                return redirect('confirmationInscription')
            except ValidationError as e:
                student_form.add_error('description', e.message)
    else:
        user_form = UserForm()
        student_form = StudentRegistrationForm()

    context = {
        'user_form': user_form,
        'student_form': student_form
    }
    return render(request, 'Accounts/student_form.html', context)


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