from django import forms

from .models import Company, Mission, PAYMENT_CHOICES, SPECIALTY_CHOICES, Specialty

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['first_name','last_name','name', 'email', 'contact_info']
        widgets = {
            'first_name':forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
        }