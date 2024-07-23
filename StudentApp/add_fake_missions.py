import os
import django
import random
from decimal import Decimal
from django.utils.text import slugify

# Configure the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from StudentApp.models import Company, Mission, Specialty

# Assurez-vous que vous avez des entreprises et des spécialités existantes ou créez-en quelques-unes
company_emails = ["company1@example.com", "company2@example.com", "company3@example.com"]
specialty_names = ["Développement Web", "Marketing", "Design", "Rédaction", "Data Science"]

# Create companies if they don't exist
for email in company_emails:
    Company.objects.get_or_create(
        name=f"Company {email.split('@')[0]}",
        email=email,
        contact_info="1234567890"
    )

# Create specialties if they don't exist
for name in specialty_names:
    Specialty.objects.get_or_create(name=name)

# Function to create a personalized mission description
def create_mission_description(title, specialty):
    descriptions = {
        "Développement Web": [
            "Développer une application web performante et intuitive.",
            "Créer des fonctionnalités innovantes pour notre site web.",
            "Optimiser la performance et la sécurité de notre plateforme en ligne."
        ],
        "Marketing": [
            "Concevoir et mettre en œuvre des campagnes marketing percutantes.",
            "Analyser les tendances du marché et proposer des stratégies adaptées.",
            "Développer des contenus engageants pour nos réseaux sociaux."
        ],
        "Design": [
            "Créer des designs attrayants pour nos produits et services.",
            "Améliorer l'expérience utilisateur de notre site web.",
            "Développer une identité visuelle forte et cohérente."
        ],
        "Rédaction": [
            "Rédiger des articles captivants pour notre blog.",
            "Créer des contenus de qualité pour notre site web.",
            "Développer des scripts percutants pour nos vidéos promotionnelles."
        ],
        "Data Science": [
            "Analyser des données complexes pour en extraire des insights.",
            "Développer des modèles prédictifs pour optimiser nos processus.",
            "Travailler sur des projets innovants en intelligence artificielle."
        ]
    }
    description = random.choice(descriptions.get(specialty.name, ["Travailler sur une mission passionnante dans votre domaine d'expertise."]))
    return f"{title}: {description}"

# Function to create fake missions
def create_fake_mission(company):
    specialty = Specialty.objects.order_by('?').first()

    title = f"Mission {slugify(specialty.name)} {random.randint(1, 100)}"
    description = create_mission_description(title, specialty)

    payment_type = random.choice(["cash", "equity"])
    cash_amount_min = Decimal(random.uniform(50, 1000)).quantize(Decimal('0.01'))
    cash_amount_max = cash_amount_min + Decimal(random.uniform(50, 500)).quantize(Decimal('0.01'))
    equity_offer = Decimal(random.uniform(1, 10)).quantize(Decimal('0.01'))

    mission_data = {
        "title": title,
        "description": description,
        "specialty": specialty,
        "payment_type": payment_type,
        "cash_amount_min": cash_amount_min if payment_type == "cash" else None,
        "cash_amount_max": cash_amount_max if payment_type == "cash" else None,
        "equity_offer": equity_offer if payment_type == "equity" else None,
        "company": company
    }

    return Mission(**mission_data)

# Number of fake missions to create
num_missions = len(company_emails)

# Create and save the fake missions
created_companies = set()
for _ in range(num_missions):
    company = Company.objects.order_by('?').first()
    while company in created_companies:
        company = Company.objects.order_by('?').first()

    mission = create_fake_mission(company)
    mission.save()
    created_companies.add(company)

print(f"{num_missions} fake missions have been created.")
