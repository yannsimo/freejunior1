# Dans un fichier utils.py ou un autre nom que vous préférez

from django.contrib.auth import get_user_model
from .models import Student

User = get_user_model()

def delete_fake_students():
    # Récupérer tous les faux étudiants créés (par exemple, filtrer par email fictif)
    fake_students = Student.objects.filter(user__email__contains='@example.org')

    # Supprimer chaque faux étudiant
    for student in fake_students:
        # Supprimer l'objet Student
        student.delete()

        # Supprimer l'utilisateur associé
        user = User.objects.get(id=student.user.id)
        user.delete()

        print(f'Deleted student profile for {student.user.first_name} {student.user.last_name}')

    print('All fake student profiles have been deleted.')
