from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'country', 'created_date', 'status', 'notes', 'manager']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'post_name',
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'id': 'post_phone',
                'class': 'form-control',
                'required': True,
            }),
            'email': forms.TextInput(attrs={
                'id': 'post_email',
                'class': 'form-control',
            }),
            'country': forms.TextInput(attrs={
                'id': 'post_country',
                'class': 'form-control',
            }),
            'notes': forms.Textarea(attrs={
                'id': 'post_notes',
                'class': 'form-control',
            }),
            'created_date': forms.DateTimeInput(attrs={
                'id': 'post_created_date',
                'class': 'form-control',
            }),
            'status': forms.Select(attrs={
                'id': 'post_status',
                'class': 'form-control',
            }),
            'manager': forms.Select(attrs={
                'id': 'post_manager',
                'class': 'form-control',
                'required': True
            }),
        }