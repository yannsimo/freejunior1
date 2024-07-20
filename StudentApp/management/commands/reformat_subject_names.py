from django.core.management.base import BaseCommand
from StudentApp.models import Student, School, Subject

def format_text_by_words(text, words_per_line=10):
    if not text:
        return text
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

class Command(BaseCommand):
    help = 'Reformat text fields for existing records in School, Subject, and Student models'

    def handle(self, *args, **kwargs):
        self.reformat_school_names()
        self.reformat_subject_names()
        self.reformat_student_fields()

    def reformat_school_names(self):
        schools = School.objects.all()
        for school in schools:
            original_text = school.name
            formatted_text = format_text_by_words(original_text, words_per_line=10)
            school.name = formatted_text
            school.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully reformatted school ID {school.id}'))

    def reformat_subject_names(self):
        subjects = Subject.objects.all()
        for subject in subjects:
            original_text = subject.name
            formatted_text = format_text_by_words(original_text, words_per_line=10)
            subject.name = formatted_text
            subject.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully reformatted subject ID {subject.id}'))

    def reformat_student_fields(self):
        students = Student.objects.all()
        for student in students:
            if student.school:
                original_school_name = student.school.name
                formatted_school_name = format_text_by_words(original_school_name, words_per_line=10)
                student.school.name = formatted_school_name
                student.school.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully reformatted student ID {student.id} school name'))

            if student.related_subject:
                original_subject_name = student.related_subject.name
                formatted_subject_name = format_text_by_words(original_subject_name, words_per_line=10)
                student.related_subject.name = formatted_subject_name
                student.related_subject.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully reformatted student ID {student.id} related subject name'))
