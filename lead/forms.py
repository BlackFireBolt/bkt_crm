from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'country', 'time_zone', 'created_date', 'status', 'notes', 'manager']
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
            'time_zone': forms.TextInput(attrs={
                'id': 'post_time_zone',
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


class ImportForm(forms.Form):
    name_field = forms.IntegerField(label='Номер столбца имен')
    phone_field = forms.IntegerField(label='Номер столбца телефонов')
    email_field = forms.IntegerField(label='Номер столбца электронных почт')
    file_field = forms.FileField(label='Файл в формате CSV')


class LeadManagerForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['manager']
        widgets = {
            'manager': forms.Select(attrs={
                'id': 'post_inner_manager',
                'class': 'form-control',
                'required': True
            })
        }