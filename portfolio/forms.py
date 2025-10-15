from django import forms
from .models import ContactSubmission, NewsletterSubscriber


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "subject", "message", "is_urgent"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your Email"}),
            "subject": forms.TextInput(attrs={"placeholder": "Your Subject"}),
            "message": forms.Textarea(attrs={"placeholder": "Your Message", "rows": 4}),
            "is_urgent": forms.HiddenInput(),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Enter your E-mail"}),
        }
