from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'نام شما'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'ایمیل شما'}),
            'subject': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'موضوع پیام'}),
            'message': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'rows': 5, 'placeholder': 'پیام شما'}),
        }
        labels = {
            'name': 'نام',
            'email': 'ایمیل',
            'subject': 'موضوع',
            'message': 'پیام',
        }