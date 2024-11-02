from django.urls import path
from StudentApp import views
from django.contrib import admin
urlpatterns = [
    path('', views.Pageaccueil, name='accueil'),  # Ajoutez cette ligne pour la page d'accueil
    path('admin/', admin.site.urls),  # Supprimez cette ligne, elle est déjà dans ebdjango/urls.py
    path('page_company/', views.page_company, name='page_company'),
    path('confirmationMessage/', views.confirmationMessage, name='confirmationMessage'),
    path('confirmationMessageAvis/', views.confirmationMessageAvis, name='confirmationMessageAvis'),
    path('confirmationInscription/', views.confirmationInscription, name='confirmationInscription'),
    path('confirmationEntreprise/', views.confirmationEntreprise, name='confirmationEntreprise'),
    path('page_etudiant/', views.page_etudiant, name='page_etudiant'),
    path('contact/', views.contactAvis, name='contact'),
    # path('Etudiants/', views.student_list, name='student_list'),
    path('Missions/', views.mission_list, name='mission_list'),
    path('Missions/<str:speciality_name>/', views.mission_list, name='mission_list_filter'),
    path('mission/detail/<int:mission_id>/', views.mission_detail, name='mission_detail'),
    path('mission/<int:mission_id>/apply/', views.mission_detail, name='apply_mission'),
    path('detail/<int:student_id>/', views.student_detail, name='student_detail'),
    #path('Etudiants/<str:speciality_name>/', views.student_list, name='student_list_filter'),
    #path('student/<int:student_id>/contact/', views.student_detail, name='contact_student'),
    path('terms/', views.terms_of_service, name='terms_of_service'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('submit_mission/', views.submit_mission_view, name='submit_mission'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
]