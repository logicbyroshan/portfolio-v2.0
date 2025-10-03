from django import forms
from .models import ContactSubmission, NewsletterSubscriber, CollaborationProposal

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Your Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 4}),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your E-mail'}),
        }


class CollaborationProposalForm(forms.ModelForm):
    class Meta:
        model = CollaborationProposal
        fields = ['full_name', 'email', 'github_id', 'linkedin_id', 'proposal']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Your Full Name',
                'class': 'form-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your.email@example.com',
                'class': 'form-input'
            }),
            'github_id': forms.TextInput(attrs={
                'placeholder': 'Your GitHub username (optional)',
                'class': 'form-input'
            }),
            'linkedin_id': forms.TextInput(attrs={
                'placeholder': 'LinkedIn profile URL or username (optional)',
                'class': 'form-input'
            }),
            'proposal': forms.Textarea(attrs={
                'placeholder': 'Describe your project idea, what you\'d like to collaborate on, timeline, and any other relevant details...',
                'class': 'form-textarea',
                'rows': 8
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'github_id': 'GitHub Username',
            'linkedin_id': 'LinkedIn Profile',
            'proposal': 'Project Proposal',
        }





