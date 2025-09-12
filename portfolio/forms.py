from django import forms
from .models import ContactSubmission, NewsletterSubscriber, CollaborationProposal, Resource, ResourceCategory

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


class ResourceSubmissionForm(forms.ModelForm):
    """
    Form for submitting new resource suggestions.
    """
    class Meta:
        model = Resource
        fields = [
            'title', 'description', 'resource_type', 'link', 
            'author', 'categories', 'technologies'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Resource Title',
                'class': 'form-input'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Brief description of what makes this resource valuable...',
                'class': 'form-textarea',
                'rows': 4
            }),
            'resource_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'link': forms.URLInput(attrs={
                'placeholder': 'https://example.com/resource',
                'class': 'form-input'
            }),
            'author': forms.TextInput(attrs={
                'placeholder': 'Resource Author/Creator (optional)',
                'class': 'form-input'
            }),
            'categories': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-checkbox-group'
            }),
            'technologies': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-checkbox-group'
            }),
        }
        labels = {
            'title': 'Resource Title',
            'description': 'Description',
            'resource_type': 'Resource Type',
            'link': 'Resource URL',
            'author': 'Author/Creator',
            'categories': 'Categories',
            'technologies': 'Related Technologies',
        }


class ResourceFilterForm(forms.Form):
    """
    Form for filtering resources on the resources page.
    """
    category = forms.ModelChoiceField(
        queryset=ResourceCategory.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'onchange': 'this.form.submit()'
        })
    )
    
    resource_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Resource.ResourceType.choices),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'onchange': 'this.form.submit()'
        })
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search resources...',
            'class': 'form-input'
        })
    )