
from django.urls import reverse
from Accounts.FormsEtudiant import StudentRegistrationForm
from .FormsEntreprise import MissionForm,EntrepriseForm
from .ContactForm import ContactForm,ContactFormAvis
from StudentApp import navigation, model_helpers
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from StudentApp.models import Student , Comment, Mission
from django.core.mail import send_mail
from .CommentForm import CreateComment


def student_list(request, speciality_name=model_helpers.student_speciality_all.slug()):
    speciality, students = model_helpers.get_speciality_Student(speciality_name)
    specialities = model_helpers.get_speciality()
    context = {
        'specialities': specialities,
        'students': students,
        'speciality': speciality,
        'navigation_items': navigation.navigation_items(navigation.NAV_FormListStudent),
    }
    return render(request, 'StudentApp/student_list.html', context)
def mission_list(request, speciality_name=model_helpers.mission_speciality_all.slug()):
    speciality, missions = model_helpers.get_speciality_Mission(speciality_name)
    specialities = model_helpers.get_speciality()
    context = {
        'specialities': specialities,
        'missions': missions,
        'speciality': speciality,
        'navigation_items': navigation.navigation_items(navigation.NAV_FormListMission),
    }
    return render(request, 'StudentApp/mission_list.html', context)


def edit_student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentRegistrationForm(instance=student)

    context = {
        'form': form,
        'student': student
    }
    return render(request, 'StudentApp/edit_student_profile.html', context)


def page_company(request):
    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_FormCompany),
    }
    return render(request, 'StudentApp/PageEntreprise.html', context)


def page_etudiant(request):
    context = {
        'navigation_items':  navigation.navigation_items(navigation.NAV_FormStudent),
    }
    return render(request, 'StudentApp/PageEtudiant.html', context)


def confirmationInscription(request):

    return render(request, 'StudentApp/ConfirmationInscription.html')
def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    comments = student.comments.exclude(status=Comment.STATUS_HIDDEN).order_by('created_at')

    if request.method == 'POST':
        comment_form = CreateComment(request.POST)
        form = ContactForm(request.POST)

        if form.is_valid():
            your_name = form.cleaned_data['your_name']
            your_email = form.cleaned_data['your_email']
            message = form.cleaned_data['message']
            subject = f"Message de {your_name} via FreeJunior"
            email_message = f"De: {your_name}\nEmail: {your_email}\n\nMessage:\n{message}"
            try:
                send_mail(subject, email_message, your_email, [student.user.email])
                send_mail(subject, email_message, your_email, ['yann-junior.simo@grenoble-inp.org'])
                messages.success(request, "Votre message a été envoyé.")
                return redirect(f"{reverse('confirmationMessage')}?name={your_name}&email={your_email}&student_name={student.user.first_name}")
            except Exception as e:
                messages.error(request, "Une erreur s'est produite lors de l'envoi de l'email.")
                return redirect(f"{reverse('confirmationMessage')}?name={your_name}&email={your_email}&student_name={student.user.first_name}")
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.student = student
            comment.save()
            messages.success(request, "Votre commentaire a été ajouté avec succès.")
    else:
        comment_form = CreateComment()
        form = ContactForm()
    context = {
        'student': student,
        'form': form,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'StudentApp/student_detail.html', context)


@permission_required('StudentApp.view_mission', raise_exception=False)
def mission_detail(request, mission_id):
    mission = get_object_or_404(Mission, pk=mission_id)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            your_name = form.cleaned_data['your_name']
            your_email = form.cleaned_data['your_email']
            message = form.cleaned_data['message']
            subject = f'Nouvelle candidature pour {mission.title}'
            email_message = f"De: {your_name}\nEmail: {your_email}\n\nMessage:\n{message}"
            try:
                send_mail(subject, email_message, your_email, [mission.company.email])
                messages.success(request, "Votre message a été envoyé.")
            except Exception as e:
                messages.error(request, "Une erreur s'est produite lors de l'envoi de l'email.")
            return redirect(
                f"{reverse('confirmationMessage')}?name={your_name}&email={your_email}&student_name={mission.company.name}")
    else:
        form = ContactForm()

    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_FormListMission),
        'mission': mission,
        'form': form,
    }
    return render(request, 'StudentApp/mission_detail.html', context)

def confirmationMessage(request):
    name = request.GET.get('name')
    email = request.GET.get('email')
    student_name = request.GET.get('student_name')
    context = {
        'name': name,
        'email': email,
        'student_name':student_name,
    }
    return render(request, 'StudentApp/confirmationMessage.html', context)

def confirmationMessageAvis(request):
    email = request.GET.get('email')
    context = {
        'email': email,
    }
    return render(request, 'StudentApp/confirmationMessageAvis.html', context)

def confirmationEntreprise(request):
    return render(request, 'StudentApp/ConfirmationEntreprise.html')

def Pageaccueil(request):
    return render(request, 'StudentApp/Accueil.html')


def contactAvis(request):
    if request.method == 'POST':
        form = ContactFormAvis(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data['telephone']
            your_email = form.cleaned_data['your_email']
            message = form.cleaned_data['message']
            categoriecontact = form.cleaned_data['categoriecontact']
            subject = f"Objet du contact : {categoriecontact} via FreeJunior"
            email_message = f"De: {telephone}\nEmail: {your_email}\n\nMessage:\n{message}"
            try:
                send_mail(subject, email_message, your_email, ['yann-junior.simo@grenoble-inp.org'])
                messages.success(request, "Votre message a été envoyé.")
                return redirect(f"{reverse('confirmationMessageAvis')}?email={your_email}")
            except Exception as e:
                messages.error(request, f"Une erreur s'est produite lors de l'envoi de l'email : {e}")
    else:
        form = ContactFormAvis()

    context = {
        'form': form,
    }
    return render(request, 'StudentApp/contactavis.html', context)


def terms_of_service(request):
    return render(request, 'StudentApp/terms_of_service.html')
def privacy_policy(request):
    return render(request, 'StudentApp/privacy_policy.html')


def submit_mission_view(request):
    if request.method == 'POST':
        entreprise_form = EntrepriseForm(request.POST)
        mission_form = MissionForm(request.POST)
        if entreprise_form.is_valid() and mission_form.is_valid():
            company = entreprise_form.save()
            mission = mission_form.save(commit=False)
            mission.company = company
            mission.save()
            print("formulaire valide")
            messages.success(request, 'Votre mission a été soumise avec succès!')
            return redirect('submit_mission')
    else:
        entreprise_form = EntrepriseForm()
        mission_form = MissionForm()


    return render(request, 'StudentApp/Entreprise_form.html', {
        'entreprise_form': entreprise_form,
        'mission_form': mission_form
    })