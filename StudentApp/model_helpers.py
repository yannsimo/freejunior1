from typing import List

from StudentApp.models import Student, Specialty,Mission

student_speciality_all = Specialty(name='')
mission_speciality_all = Specialty(name='')

def get_speciality_Student(speciality_name):
    student = Student.objects.all()
    if speciality_name == student_speciality_all.slug():
        specialty_std = student_speciality_all
    else:
        try:
            specialty_std = Specialty.objects.get(name__iexact=speciality_name)
            student = student.filter(specialty=specialty_std)
        except Specialty.DoesNotExist:
            specialty_std = Specialty(name=speciality_name)
            student = Student.objects.none()

    student = student.order_by('hourly_rate')
    return specialty_std, student

def get_speciality():
    specialities = list(Specialty.objects.all().order_by('name'))
    return specialities


def get_speciality_Mission(speciality_name):
    mission = Mission.objects.all()
    if speciality_name == mission_speciality_all.slug():
        specialty_std = mission_speciality_all
    else:
        try:
            specialty_std = Specialty.objects.get(name__iexact=speciality_name)
            mission = mission.filter(specialty=specialty_std)
        except Specialty.DoesNotExist:
            specialty_std = Specialty(name=speciality_name)
            mission = Mission.objects.none()

    mission = mission.order_by('date')
    return specialty_std, mission