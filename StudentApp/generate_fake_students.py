import os
import string
import sys
import django
import random
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from faker import Faker
from openai import OpenAI
import unicodedata
import requests
from dotenv import load_dotenv
load_dotenv()
# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreeJunior.settings')
django.setup()

from StudentApp.models import Student, School, Specialty, Program, Subject
from django.contrib.auth import get_user_model

User = get_user_model()

# Configuration de l'API OpenAI

# Instances de Faker pour différentes locales
fake_fr = Faker('fr_FR')
fake_african = Faker('en_US')  # Using en_US as a representation of African names in Faker
fake_european = Faker('en_GB')  # Using en_GB as a representation of European names in Faker
fake = Faker()

# Listes de prénoms et noms arabes translittérés
arabic_first_names = [
    "Mohamed", "Ahmed", "Youssef", "Ali", "Hassan", "Omar", "Ayman", "Said", "Rachid", "Ibrahim"
]
arabic_last_names = [
    "Ben Ali", "El Masry", "El Fassi", "Al Harbi", "Abdel Rahman", "Ibn Sina", "Al Amari", "El Sayed", "Al Mansour",
    "Ben Youssef"
]
specialties_data = {
    "Développement web et mobile": {
        "écoles": ["Université Grenoble Alpes", "Polytech Grenoble", "MydigitalSchool"],
        "programmes": ["Licence Informatique", "Master Développement Web", "Bachelor Développement Mobile",
                       "Diplôme d'ingénieur en Informatique"],
        "sujets": [
            ["HTML/CSS", "JavaScript", "React", "Node.js"],
            ["Swift", "Kotlin", "Objective-C"],
            ["PHP", "Angular", "Vue.js"]
        ]
    },
    "Data Science et IA": {
        "écoles": ["Université Grenoble Alpes"],
        "programmes": ["Master Data Science", "MSc Intelligence Artificielle", "Diplôme d'ingénieur en Data Science"],
        "sujets": [
            ["Python pour Data Science", "Machine Learning", "Deep Learning"],
            ["Big Data Analytics", "Natural Language Processing"]
        ]
    },

"Marketing digital": {
        "écoles": ["Digital College","WIS - Web International School","Ecole Studio M","Grenoble Ecole de Management","MyDigitalSchool"],
        "programmes": ["Bachelor Marketing Digital", "MBA Marketing Digital"],
        "sujets": [
            ["SEO/SEM", "Social Media Marketing", "Content Marketing"],
            ["Google Analytics", "Email Marketing", "Inbound Marketing"]
        ]
},
"E-commerce": {
        "écoles": ["Digital College","WIS - Web International School","Ecole Studio M","Grenoble Ecole de Management","MyDigitalSchool"],
        "programmes": ["Bachelor E-commerce", "MBA Stratégie E-commerce"],
        "sujets": [
        ["Gestion de boutique en ligne", "Optimisation de conversion", "Logistique e-commerce"],
        ["Paiement en ligne", "CRM pour e-commerce", "Marketplaces"]
        ]
},
"Data Marketing": {
        "écoles": ["Digital College","WIS - Web International School","Ecole Studio M","Grenoble Ecole de Management","MyDigitalSchool"],
        "programmes": ["Bachelor Data Marketing", "MSc Big Data & Marketing"],
        "sujets": [
        ["Analyse prédictive", "Segmentation client", "Data visualisation"],
        ["Machine Learning pour le marketing", "Attribution marketing", "RGPD et éthique des données"]
        ]
},
"Communication digitale": {
        "écoles": ["Digital College","WIS - Web International School","Ecole Studio M","Grenoble Ecole de Management","MyDigitalSchool"],
        "programmes": ["Bachelor Communication Digitale", "Mastère Stratégie de Communication Digitale"],
        "sujets": [
        ["Storytelling digital", "Personal branding", "Gestion de communauté"],
        ["Relations presse digitales", "Influence marketing", "Communication de crise en ligne"]
        ]
},
"Transformation digitale": {
    "écoles": ["Digital College","WIS - Web International School","Ecole Studio M","Grenoble Ecole de Management","MyDigitalSchool"],
    "programmes": ["MSc Transformation Digitale", "MBA Innovation Digitale"],
    "sujets": [
    ["Stratégie digitale", "Conduite du changement", "Nouveaux modèles d'affaires"],
    ["Technologies disruptives", "Agilité organisationnelle", "Leadership digital"]
    ]
},
    "Développement Django": {
        "écoles": ["Grenoble INP - Ensimag"],
        "programmes": ["Ingénierie pour la finance", "Ingénierie des systèmes d'informatique", "MMIS"],
        "sujets": [
            ["Django", "Python", "HTML/CSS", "JavaScript"],
            ["SQL", "REST APIs", "React", "Node.js"]
        ]
    },
    "Gestion de bases de données": {
        "écoles": ["Grenoble INP - Ensimag"],
        "programmes": ["Ingénierie pour la finance", "Ingénierie des systèmes d'informatique", "MMIS"],
        "sujets": [
            ["SQL", "NoSQL", "Database Administration"],
            ["MongoDB", "MySQL", "PostgreSQL"]
        ]
    },
    "Développement Java": {
        "écoles": ["Grenoble INP - Ensimag"],
        "programmes": ["Ingénierie pour la finance", "Ingénierie des systèmes d'informatique", "MMIS"],
        "sujets": [
            ["Java SE", "Java EE", "Spring Framework"],
            ["Hibernate", "JUnit", "Microservices"]
        ]
    },
    "Développement Python": {
        "écoles": ["Grenoble INP - Ensimag"],
        "programmes": ["Ingénierie pour la finance", "Ingénierie des systèmes d'informatique", "MMIS"],
        "sujets": [
            ["Python", "Flask", "Django"],
            ["Data Science with Python", "Web Scraping", "Python GUI"]
        ]
    },
    "Développement Node.js": {
        "écoles": ["Grenoble INP - Ensimag"],
        "programmes": ["Ingénierie pour la finance", "Ingénierie des systèmes d'informatique", "MMIS"],
        "sujets": [
            ["Node.js", "Express.js", "RESTful APIs"],
            ["MongoDB", "MySQL", "Socket.io"]
        ]
    },
    "Audiovisuel": {
        "écoles": ["Université Grenoble Alpes", "École Supérieure d'Art et Design Grenoble-Valence"],
        "programmes": ["Licence Audiovisuel", "Master Cinématographie", "Bachelor Production Vidéo"],
        "sujets": [
            ["Montage vidéo", "Motion Design", "Production audio"],
            ["Ingénierie du son", "Cinématographie", "Production vidéo"]
        ]
    },
    "Systèmes de gestion de contenu (CMS)": {
        "écoles":  ["Digital College","WIS - Web International School","Ecole Studio M","Grenoble Ecole de Management","MyDigitalSchool"],
        "programmes": ["web design ", "Master Systèmes d'Information", "MBA en Informatique de Gestion", "Developppement web"],
        "sujets": [
            ["WordPress", "Drupal", "Joomla"],
            ["CMS Security", "Content Management", "Custom Themes"]
        ]
    }
}



def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def generate_student_description(school_name, specialty_name, program_name, study_level, first_name, last_name,
                                 subjects, hourly_rate):
    try:
        # Suppression des accents pour éviter les problèmes d'encodage
        school_name = remove_accents(school_name)
        specialty_name = remove_accents(specialty_name)
        program_name = remove_accents(program_name)
        study_level = remove_accents(study_level)
        first_name = remove_accents(first_name)
        last_name = remove_accents(last_name)

        # Check if subjects is a list and join them into a string
        if isinstance(subjects, list):
            subject_str = ", ".join(subjects)
        else:
            subject_str = str(subjects)  # Convert to string if not already

        subject_str = remove_accents(subject_str)

        prompt = (
            f"Je m'appelle {first_name} {last_name}. Je suis étudiant à {school_name} dans la filière {program_name} et je souhaite m'inscrire sur un site de freelance pour étudiants. "
            f"Peux-tu me dire comment faire une description sachant que j'ai choisi {specialty_name} comme spécialité que je souhaite exercer sur ce site. Je suis en {study_level} et j'étudie des sujets tels que: {subject_str}. Mon taux horaire est de {hourly_rate} euros par heure."
            f"Fais un description en inventant un stage que j'ai fait    et faites comme si c'était moi qui écrivait, je ne veux pas qu'on sache que c'est toi qui l'écrit je ne veux plus que tu écrive .")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Vous êtes un assistant chargé de créer des descriptions d'étudiants pour un site de freelance."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erreur lors de la génération de la description : {str(e)}")
        return f"Description non disponible en raison d'une erreur : {str(e)}"


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


def create_fake_student():
    choice = random.choices(['french', 'arabic', 'african', 'european'], [0.5, 0.2, 0.1, 0.1])[0]

    if choice == 'arabic':
        first_name = random.choice(arabic_first_names)
        last_name = random.choice(arabic_last_names)
    elif choice == 'african':
        first_name = fake_african.first_name()
        last_name = fake_african.last_name()
    elif choice == 'european':
        first_name = fake_european.first_name()
        last_name = fake_european.last_name()
    else:
        first_name = fake_fr.first_name()
        last_name = fake_fr.last_name()

    email = fake.unique.email()
    password = generate_random_password()

    user = User.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )

    specialty = random.choice(list(specialties_data.keys()))
    school = random.choice(specialties_data[specialty]["écoles"])
    program = random.choice(specialties_data[specialty]["programmes"])
    subject = random.choice(specialties_data[specialty]["sujets"])
    study_level = random.choice(Student.STUDY_LEVEL_CHOICES)[0]
    hourly_rate = round(random.uniform(11.0, 30), 2)

    description = generate_student_description(school, specialty, program, study_level, first_name, last_name, subject,
                                               hourly_rate)

    if isinstance(subject, list):
        subject_str = ", ".join(subject)
    else:
        subject_str = str(subject)
    school_obj, _ = School.objects.get_or_create(name=school)
    specialty_obj, _ = Specialty.objects.get_or_create(name=specialty)
    program_obj, _ = Program.objects.get_or_create(name=program, school=school_obj)
    subject_obj, _ = Subject.objects.get_or_create(name=subject_str, program=program_obj)

    student = Student.objects.create(
        user=user,
        study_level=study_level,
        hourly_rate=hourly_rate,
        description=description,
        school=school_obj,
        specialty=specialty_obj,
        program=program_obj,
        related_subject=subject_obj
    )
    student.save()

    print(f'Created student profile for {first_name} {last_name} in {specialty} at {school}')


def main():
    num_students = 15
    for _ in range(num_students):
        create_fake_student()


if __name__ == "__main__":
    main()
