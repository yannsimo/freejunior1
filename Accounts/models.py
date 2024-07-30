from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Les utilisateurs doivent avoir une adresse e-mail')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        extra_fields.setdefault('staff', True)
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('admin', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    # Champs communs
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    # Champs spécifiques à l'entreprise
    company_name = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    # Champ pour distinguer le type d'utilisateur
    USER_TYPE_CHOICES = (
        ('STUDENT', 'Étudiant'),
        ('COMPANY', 'Entreprise'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def get_full_name(self):
        if self.user_type == 'STUDENT':
            return f"{self.first_name} {self.last_name}"
        elif self.user_type == 'COMPANY':
            return self.company_name
        return self.email

    def get_short_name(self):
        if self.user_type == 'STUDENT':
            return self.first_name
        elif self.user_type == 'COMPANY':
            return self.company_name
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_student(self):
        return self.user_type == 'STUDENT'

    @property
    def is_company(self):
        return self.user_type == 'COMPANY'