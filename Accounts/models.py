from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Crée et enregistre un utilisateur avec l'email, le prénom, le nom de famille et le mot de passe donnés.
        """
        if not email:
            raise ValueError('Les utilisateurs doivent avoir une adresse e-mail')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        """
        Crée et enregistre un utilisateur du staff avec l'email, le prénom, le nom de famille et le mot de passe donnés.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Crée et enregistre un superutilisateur avec l'email, le prénom, le nom de famille et le mot de passe donnés.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,  PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(default=True)  # L'utilisateur peut se connecter si is_active=True
    staff = models.BooleanField(default=False)  # Un membre du personnel non admin
    admin = models.BooleanField(default=False)  # Un superutilisateur

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Email et Password sont requis par défaut

    def get_full_name(self):
        """
        L'utilisateur est identifié par son adresse email
        """
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        """
        L'utilisateur est identifié par son adresse email
        """
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        L'utilisateur a-t-il une autorisation spécifique ?
        """
        return True

    def has_module_perms(self, app_label):
        """
        L'utilisateur dispose-t-il des autorisations nécessaires pour voir l'application `app_label` ?
        """
        return True

    @property
    def is_staff(self):
        """
        L'utilisateur est-il un membre du personnel ?
        """
        return self.staff

    @property
    def is_admin(self):
        """
        L'utilisateur est-il un administrateur ?
        """
        return self.admin