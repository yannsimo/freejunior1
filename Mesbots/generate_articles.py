import openai
from faker import Faker
from django.core.management.base import BaseCommand
from StudentApp.models import Article

# Configuration de l'API OpenAI
openai.api_key = "YOUR_OPENAI_API_KEY"
fake = Faker()

def generate_article_content():
    prompt = "Écrire un article sur les avantages du freelancing pour les étudiants."
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

def generate_article_title():
    topics = [
        "Les avantages du freelancing pour les étudiants",
        "Comment le freelancing aide les étudiants à gagner de l'argent",
        "Opportunités de freelancing pour les étudiants",
        "Le freelancing comme solution pour les étudiants en difficulté financière"
    ]
    return fake.sentence(ext_word_list=topics)

def post_article():
    title = generate_article_title()
    content = generate_article_content()
    article = Article(
        title=title,
        content=content,
        tags="freelance, étudiants, emploi, application",
        author="Votre Nom"
    )
    article.save()

class Command(BaseCommand):
    help = 'Generate and post an article'

    def handle(self, *args, **kwargs):
        post_article()
        self.stdout.write(self.style.SUCCESS('Article généré et publié avec succès'))
