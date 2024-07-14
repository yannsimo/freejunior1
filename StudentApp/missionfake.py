import os
import sys
import django

# Configurez l'environnement Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreeJunior.settings')
django.setup()

import openai
from StudentApp.FormsEntreprise import EntrepriseForm, MissionForm
from StudentApp.models import Company, Mission, Specialty

# Configurez votre clé API OpenAI


def get_detailed_description(title, specialty):
    prompt = f"Écrivez une description détaillée pour une mission de {specialty} intitulée '{title}'. La description doit inclure les objectifs, les compétences requises, et les livrables attendus. La description doit faire entre 100 et 150 mots."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Vous êtes un expert en rédaction d'offres d'emploi et de missions freelance."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API OpenAI: {e}")
        return "Description non disponible en raison d'une erreur."


def create_fake_missions():
    # Créer une fausse entreprise
    company_data = {
        'name': 'TechInnovate Solutions',
        'email': 'contac@techinnovate.com',
        'contact_info': '0123456789'
    }
    company_form = EntrepriseForm(data=company_data)
    if company_form.is_valid():
        company = company_form.save()
    else:
        print("Erreur dans la création de l'entreprise:", company_form.errors)
        return

    # Créer des fausses missions
    fake_missions = [
        {
            'title': 'Développement d\'une application mobile de gestion de projets',
            'specialty_name': 'DEV',
            'payment_type': 'hourly'
        },
        {
            'title': 'Campagne de marketing digital pour un lancement de produit',
            'specialty_name': 'MARK',
            'payment_type': 'fixed'
        },
        {
            'title': 'Analyse prédictive des comportements clients',
            'specialty_name': 'DATA',
            'payment_type': 'hourly'
        }
    ]

    for mission_data in fake_missions:
        # Obtenir une description détaillée via l'API ChatGPT
        detailed_description = get_detailed_description(mission_data['title'], mission_data['specialty_name'])

        mission_data['description'] = detailed_description

        mission_form = MissionForm(data=mission_data)
        if mission_form.is_valid():
            mission = mission_form.save(commit=False)
            mission.company = company
            mission.save()
            print(f"Mission créée: {mission.title}")
            print(f"Description: {mission.description[:100]}...")  # Affiche les 100 premiers caractères
        else:
            print(f"Erreur dans la création de la mission {mission_data['title']}:", mission_form.errors)


if __name__ == "__main__":
    create_fake_missions()