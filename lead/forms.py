from django import forms

from .models import Lead, Note, Notification, Task


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'country', 'time_zone', 'created_date', 'status', 'manager',
                  'source', 'utm', 'depozit']
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
            'depozit': forms.TextInput(attrs={
                'id': 'post_depozit',
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
            'source': forms.TextInput(attrs={
                'id': 'post_source',
                'class': 'form-control',
            }),
            'utm': forms.TextInput(attrs={
                'id': 'post_utm',
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


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text', ]
        widgets = {
            'text': forms.Textarea(attrs={
                'id': 'post_note',
                'class': 'form-control',
                'placeholder': 'Добавить'
            }),
        }


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['text', 'time']
        widgets = {
            'text': forms.Textarea(attrs={
                'id': 'post_notification',
                'class': 'form-control',
                'placeholder': 'Текст',
                'required': True
            }),
            'time': forms.DateTimeInput(attrs={
                'id': 'post_time',
                'class': 'form-control',
                'placeholder': 'Дата и время',
                'required': True
            }),
        }


class ImportForm(forms.Form):
    name_field = forms.IntegerField(label='Номер столбца имен')
    phone_field = forms.IntegerField(label='Номер столбца телефонов')
    email_field = forms.IntegerField(label='Номер столбца электронных почт')
    notes_field = forms.IntegerField(label='Номер столбца заметок')
    agreements_field = forms.IntegerField(label='Номер столбца договоренностей')
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


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['text', 'expiration_time', 'manager']
        widgets = {
            'manager': forms.Select(attrs={
                'id': 'task_manager',
                'class': 'form-control',
                'required': True
            }),
            'text': forms.Textarea(attrs={
                'id': 'task_text',
                'class': 'form-control',
                'required': True
            }),
            'expiration_time': forms.DateTimeInput(attrs={
                'id': 'task_expiration_time',
                'class': 'form-control',
                'placeholder': 'Дата и время',
                'required': True
            }),
        }