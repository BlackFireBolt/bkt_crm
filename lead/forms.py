from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'country', 'created_date', 'status', 'notes', 'manager']
