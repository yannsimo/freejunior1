from django import forms
class ContactForm(forms.Form):
    your_name = forms.CharField(max_length=100, label="Votre nom")
    your_email = forms.EmailField(label="Votre email")
    message = forms.CharField(widget=forms.Textarea, label="Votre message")


class ContactFormAvis(forms.Form):
    categorie = [
        ('support', 'Support'),
        ('feedback', 'Feedback'),
        ('general', 'General'),
    ]
    telephone = forms.CharField(
        max_length=100,
        label="Votre numéro de téléphone ",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre numéro de téléphone'})
    )
    your_email = forms.EmailField(
        label="Votre email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'})
    )
    categoriecontact = forms.ChoiceField(
        label="Veuillez sélectionner l'objet de votre appel",
        choices=categorie,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre message', 'rows': 4}),
        label="Votre message"
    )