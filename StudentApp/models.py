
from unittest import TestCase
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.template.defaultfilters import slugify, date
from django.contrib.auth  import get_user_model
User = get_user_model()

SPECIALTY_CHOICES = [
    ('developpement_web', 'Développement Web'),
    ('mobile_app_development', 'Développement d\'applications mobiles'),
    ('software_development', 'Développement de logiciels'),
    ('front_end_development', 'Développement Front-end'),
    ('back_end_development', 'Développement Back-end'),
    ('full_stack_development', 'Développement Full-stack'),
    ('cloud_computing', 'Cloud Computing'),
    ('devops', 'DevOps'),
    ('data_science', 'Data Science'),
    ('machine_learning', 'Apprentissage automatique (Machine Learning)'),
    ('artificial_intelligence', 'Intelligence artificielle'),
    ('blockchain', 'Blockchain'),
    ('cyber_security', 'Sécurité informatique (Cyber sécurité)'),
    ('networking', 'Réseaux informatiques'),
    ('database_management', 'Gestion de bases de données'),
    ('systems_architecture', 'Architecture des systèmes'),
    ('ui_ux_design', 'Conception UI/UX'),
    ('game_development', 'Développement de jeux vidéo'),
    ('iot', 'Internet des objets (IoT)'),
    ('robotics', 'Robotique'),
    ('virtual_reality', 'Réalité virtuelle'),
    ('augmented_reality', 'Réalité augmentée'),
    ('3d_modeling', 'Modélisation 3D'),
    ('computer_graphics', 'Graphisme informatique'),
    ('computer_vision', 'Vision par ordinateur'),
    ('embedded_systems', 'Systèmes embarqués'),
    ('enterprise_software', 'Logiciels d\'entreprise'),
    ('web_scraping', 'Web Scraping'),
    ('data_analysis', 'Analyse de données'),
    ('business_intelligence', 'Intelligence d\'affaires'),
    ('erp', 'ERP (Planification des ressources de l\'entreprise)'),
    ('crm', 'CRM (Gestion de la relation client)'),
    ('e-commerce', 'E-commerce'),
    ('wordpress_development', 'Développement WordPress'),
    ('shopify_development', 'Développement Shopify'),
    ('magento_development', 'Développement Magento'),
    ('prestashop_development', 'Développement PrestaShop'),
    ('django_development', 'Développement Django'),
    ('flask_development', 'Développement Flask'),
    ('laravel_development', 'Développement Laravel'),
    ('ruby_on_rails_development', 'Développement Ruby on Rails'),
    ('nodejs_development', 'Développement Node.js'),
    ('react_development', 'Développement React'),
    ('angular_development', 'Développement Angular'),
    ('vuejs_development', 'Développement Vue.js'),
    ('typescript_development', 'Développement TypeScript'),
    ('java_development', 'Développement Java'),
    ('python_development', 'Développement Python'),
    ('csharp_development', 'Développement C#'),
    ('php_development', 'Développement PHP'),
    ('cpp_development', 'Développement C++'),
    ('rust_development', 'Développement Rust'),
    ('golang_development', 'Développement Go (Golang)'),
    ('swift_development', 'Développement Swift'),
    ('kotlin_development', 'Développement Kotlin'),
    ('scala_development', 'Développement Scala'),
    ('typescript_development', 'Développement TypeScript'),
    ('ruby_development', 'Développement Ruby'),
    ('perl_development', 'Développement Perl'),
    ('bash_scripting', 'Scripting Bash'),
    ('powershell_scripting', 'Scripting PowerShell'),
    ('linux_system_administration', 'Administration système Linux'),
    ('windows_system_administration', 'Administration système Windows'),
    ('macos_system_administration', 'Administration système macOS'),
    ('unix_system_administration', 'Administration système Unix'),
    ('it_support', 'Support informatique'),
    ('helpdesk_support', 'Support Helpdesk'),
    ('technical_documentation', 'Documentation technique'),
    ('technical_support', 'Support technique'),
    ('quality_assurance', 'Assurance qualité'),
    ('test_automation', 'Automatisation des tests'),
    ('virtualization', 'Virtualisation'),
    ('containerization', 'Conteneurisation'),
    ('microservices', 'Microservices'),
    ('serverless_architecture', 'Architecture serverless'),
    ('big_data', 'Big Data'),
    ('data_engineering', 'Ingénierie des données'),
    ('data_migration', 'Migration des données'),
    ('data_warehousing', 'Entrepôt de données (Data Warehousing)'),
    ('etl', 'ETL (Extract, Transform, Load)'),
    ('business_analysis', 'Analyse commerciale'),
    ('project_management', 'Gestion de projet'),
    ('agile_methodologies', 'Méthodologies Agile'),
    ('scrum_master', 'Scrum Master'),
    ('product_owner', 'Product Owner'),
    ('technical_lead', 'Lead technique'),
    ('consulting', 'Consultant informatique'),
    ('freelance', 'Freelance informatique'),

    # Spécialités en audiovisuel
    ('video_editing', 'Montage vidéo'),
    ('motion_graphics', 'Motion Design'),
    ('audio_production', 'Production audio'),
    ('sound_engineering', 'Ingénierie du son'),
    ('cinematography', 'Cinématographie'),
    ('video_production', 'Production vidéo'),
    ('photography', 'Photographie'),
    ('graphic_design', 'Design graphique'),

    # Systèmes de gestion de contenu (CMS)
    ('wordpress', 'WordPress'),
    ('drupal', 'Drupal'),
    ('joomla', 'Joomla'),

    # Marketing digital et communication
    ('digital_marketing', 'Marketing digital'),
    ('social_media_management', 'Gestion des réseaux sociaux'),
    ('content_marketing', 'Marketing de contenu'),
    ('seo', 'SEO (Optimisation pour les moteurs de recherche)'),
    ('sem', 'SEM (Marketing sur les moteurs de recherche)'),
    ('email_marketing', 'Marketing par email'),
    ('affiliate_marketing', 'Marketing par affiliation'),
    ('branding', 'Branding'),
    ('community_management', 'Community Management'),
    ('copywriting', 'Rédaction publicitaire'),
    ('technical_writing', 'Rédaction technique'),
    ('visual_communication', 'Communication visuelle'),
    ('public_relations', 'Relations publiques'),
    ('event_management', 'Gestion d\'événements'),
    ('advertising', 'Publicité'),
    ('sales', 'Ventes'),
    ('business_development', 'Développement commercial'),
    ('customer_service', 'Service clientèle'),
    ('telecommunications', 'Télécommunications'),
    ('network_security', 'Sécurité réseau'),
]

PAYMENT_CHOICES = [
    ('cash', 'argent'),
    ('equity', 'Parts d\'entreprise')
]

class School(models.Model):
    name = models.CharField(max_length=255)#à formater

    def __str__(self):
        return self.name

class Specialty(models.Model):
    name = models.CharField(max_length=100)
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.get_human_readable_name()

    def get_human_readable_name(self):
        return dict(SPECIALTY_CHOICES).get(self.name,  self.name)

class Program(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='programs')

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class Student(models.Model):
    STUDY_LEVEL_CHOICES = [
        ('Bac+3', 'Bac+3'),
        ('Bac+4', 'Bac+4'),
        ('Bac+5', 'Bac+5'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    study_level = models.CharField(max_length=5, choices=STUDY_LEVEL_CHOICES, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students', null=True)#à formater
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='students', null=True)
    related_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)# à formater
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    description = models.TextField(null=True)
    photo = models.ImageField(upload_to='student_photos/', null=True)
    cv = models.FileField(upload_to='student_cvs/', blank=True, null=True)
    portfolio_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    contact_info = models.TextField()
    def __str__(self):
        return self.name



class Mission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True,default=None)  # Définit l'étudiant par défaut à None
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='missions')
    specialty= models.ForeignKey(Specialty, on_delete=models.CASCADE, null=True)
    payment_type = models.CharField(max_length=6, choices=PAYMENT_CHOICES,null=True)
    cash_amount_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cash_amount_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    equity_offer = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    disponible = models.BooleanField(default=True)
    def __str__(self):
        return self.title
class Comment(models.Model):
    STATUS_VISIBLE = 'visible'
    STATUS_HIDDEN = 'hidden'
    STATUS_MODERATED = 'moderated'

    STATUS_CHOICES = (
        (STATUS_VISIBLE, 'Visible'),
        (STATUS_HIDDEN, 'Hidden'),
        (STATUS_MODERATED, 'Moderated'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='comments')
    company_name = models.CharField(max_length=100)
    mission_title = models.CharField(max_length=100)
    text = models.TextField()
    status = models.CharField(max_length=20, default=STATUS_VISIBLE, choices=STATUS_CHOICES)
    moderation_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {} (status={})'.format(self.company_name, self.text[:20], self.status)


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title