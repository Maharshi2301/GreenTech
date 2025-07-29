from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import GreenPost
from .models import ContactMessage, ReportIssue, Feedback
from .models import VolunteerRequest, Event, VolunteerApplication


class GreenPostForm(forms.ModelForm):
    class Meta:
        model = GreenPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter your message'}),
        }

class VolunteerRequestForm(forms.ModelForm):
    class Meta:
        model  = VolunteerRequest
        fields = ['name', 'email', 'phone_number', 'area_of_interest', 'availability']
        widgets = {
            'name':             forms.TextInput(attrs={'class':'form-control'}),
            'email':            forms.EmailInput(attrs={'class':'form-control'}),
            'phone_number':     forms.TextInput(attrs={'class':'form-control'}),
            'area_of_interest': forms.TextInput(attrs={'class':'form-control'}),
            'availability':     forms.TextInput(attrs={'class':'form-control'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your feedback here...'})
        }


class ReportIssueForm(forms.ModelForm):
    class Meta:
        model = ReportIssue
        fields = ['name', 'issue']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'issue': forms.Textarea(attrs={'class': 'form-control'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']


class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ['event', 'motivation']
        widgets = {
            'event': forms.HiddenInput(),
            'motivation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }