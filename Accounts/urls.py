"""
URL configuration for FreeJunior_version1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Accounts import  views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('FormulaireEtudiant/', views.register_student, name='student_form'),
    path('login/', views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('edit_profile/', views.edit_student_profile, name='edit_student_profile'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)