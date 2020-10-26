from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import TemplateView
import json, csv, phonenumbers
from phonenumbers import timezone
from django.contrib.postgres.search import SearchVector
import logging

logger = logging.getLogger(__name__)

from . import models
from .forms import LeadForm, ImportForm, LeadManagerForm, NoteForm, NotificationForm
from braces.views import GroupRequiredMixin


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


class ListLeadJson(LoginRequiredMixin, BaseDatatableView):
    model = models.Lead
    login_url = '/login/'

    columns = ['id', 'name', 'email', 'phone', 'country', 'created_date', 'status']

    def get_initial_queryset(self):
        return models.Lead.objects.exclude(status='d').filter(manager=self.request.user.id)


class ListLead(LoginRequiredMixin, TemplateView):
    template_name = 'lead_list.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(ListLead, self).get_context_data(**kwargs)
        context['form'] = LeadForm()
        return context


class AdminListLeadJson(GroupRequiredMixin, BaseDatatableView):
    model = models.Lead
    login_url = '/login/'
    group_required = [u'Администратор', u'admin']

    def get_initial_queryset(self):
        return models.Lead.objects.exclude(status='d')

    def filter_queryset(self, qs):
        query = self.request.GET.get(u'search[value]', None)
        if query:
            search_vector = SearchVector('id', 'name', 'phone', 'email', 'depozit', 'country', 'created_date', 'status',
                                         'manager')
            qs = models.Lead.objects.annotate(search=search_vector).filter(search=query).exclude(status='d')
        return qs


class AdminListLead(GroupRequiredMixin, TemplateView):
    template_name = 'lead_list_admin.html'
    login_url = '/login/'
    group_required = [u'Администратор', u'admin']

    def get_context_data(self, **kwargs):
        context = super(AdminListLead, self).get_context_data(**kwargs)
        context['form'] = LeadForm()
        context['import_form'] = ImportForm()
        context['manager_form'] = LeadManagerForm()
        return context


@login_required(login_url='/login/')
def lead_detail(request, pk):
    lead = get_object_or_404(models.Lead, pk=pk)
    lead_form = LeadForm(instance=lead)
    notes_form = NoteForm()
    notification_form = NotificationForm()
    notes = models.Note.objects.filter(lead=pk)
    notifications = models.Notification.objects.filter(lead=pk).order_by('-id')[:2][::-1]
    context = {'lead': lead, 'lead_form': lead_form, 'notes': notes, 'notes_form': notes_form,
               'notification_form': notification_form, 'notifications': notifications}
    return render(request, 'lead_detail.html', context)


@csrf_exempt
def add_lead_post(request):
    print(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        lead = models.Lead(name=data.name, phone=data.phone, email=data.email, country=data.country,
                           created_date=models.parse_datetime(data.created_date), source='land')
        lead.save()
        return HttpResponse(status=200)


@login_required(login_url='/login/')
def add_lead(request):
    if request.method == 'POST':
        print(request.POST)
        time_zone = "None"
        country = "None"
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        try:
            if phonenumbers.is_valid_number(phone):
                p = phonenumbers.parse(phone)
                time_zone = timezone.time_zones_for_number(p)
                country = phonenumbers.region_code_for_number(p)
        except (AttributeError, ValueError, Exception):
            pass
        email = request.POST.get('email')
        created_date = request.POST.get('created_date')
        status = request.POST.get('status')
        if request.POST.get('manager') is not None:
            manager_id = request.POST.get('manager')
        else:
            manager_id = request.user.id

        lead = models.Lead(name=name, phone=phone, email=email, country=country, time_zone=time_zone,
                           created_date=created_date, status=status, manager=models.User.objects.get(id=manager_id))
        lead.save()
        manager = None
        if lead.manager:
            manager = lead.manager.username
        content = {
            'id': lead.pk,
            'name': lead.name,
            'email': lead.email,
            'depozit': lead.depozit,
            'phone': lead.phone,
            'country': lead.country,
            'created_date': models.json_serial(lead.created_date),
            'status': lead.status,
            'manager': manager,
            'type': "data.new",
        }
        response_data = {'result': 'Lead create successful', 'flag': 'new', 'content': content}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required(login_url='/login/')
def change_lead(request):
    if request.method == 'POST':
        leadpk = request.POST.get('leadpk')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        time_zone = request.POST.get('time_zone')
        email = request.POST.get('email')
        depozit = request.POST.get('depozit')
        country = request.POST.get('country')
        created_date = request.POST.get('created_date')
        status = request.POST.get('status')
        manager_id = request.POST.get('manager')

        lead = models.Lead.objects.get(pk=leadpk)
        lead.name = name
        if request.user.groups.filter(name='Администратор').exists():
            lead.phone = phone
        lead.email = email
        lead.depozit = depozit
        lead.country = country
        lead.created_date = created_date
        lead.status = status
        managerold_id = None
        if lead.manager is not None:
            managerold_id = lead.manager.id
        lead.time_zone = time_zone
        if manager_id is not None:
            lead.manager = models.User.objects.get(id=manager_id)
        if managerold_id == request.user.id or request.user.groups.filter(name='Администратор').exists():
            lead.save()
        else:
            response_data = {'result': 'User not match', 'flag': 'error'}
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        response_data = {'result': 'Lead create successful', 'flag': 'change'}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required(login_url='/login/')
def add_import(request):
    if request.method == "POST":
        response_data = {}
        reader = csv.reader(request.FILES['file_field'].read().decode('utf-8').splitlines())
        for row in reader:
            name = "None"
            email = "None"
            country = "None"
            time_zone = "None"
            if int(request.POST.get('name_field')) != 0:
                name = row[int(request.POST.get('name_field')) - 1]
            if int(request.POST.get('email_field')) != 0:
                email = row[int(request.POST.get('email_field')) - 1]
            if int(request.POST.get('notes_field')) != 0:
                notes = row[int(request.POST.get('notes_field')) - 1]
            if int(request.POST.get('agreements_field')) != 0:
                agreements = row[int(request.POST.get('agreements_field')) - 1]
            phone = ''.join(filter(str.isdigit, row[int(request.POST.get('phone_field')) - 1]))
            try:
                if phonenumbers.is_valid_number(phone):
                    p = phonenumbers.parse(phone)
                    time_zone = timezone.time_zones_for_number(p)
                    country = phonenumbers.region_code_for_number(p)
            except (AttributeError, ValueError, Exception):
                pass
            lead = models.Lead(name=name, email=email, phone=phone, country=country, time_zone=time_zone)
            lead.save()
            response_data = {'result': 'Lead create successful', 'flag': 'new'}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required(login_url='/login/')
def add_manager(request):
    if request.method == 'POST':
        manager = models.User.objects.get(id=request.POST.get('manager'))
        for data in request.POST.getlist('data[]'):
            lead = models.Lead.objects.get(pk=remove_html_tags(data))
            lead.manager = manager
            lead.save()
        response_data = {'result': 'success'}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required(login_url='/login/')
def add_note(request):
    if request.method == 'POST':
        lead_id = request.POST.get('lead_id')
        note_text = request.POST.get('note_data')
        response_data = {}

        note_object = models.Note(lead_id=lead_id, text=note_text)
        note_object.save()

        response_data['result'] = 'Create note successful!'
        response_data['note_text'] = note_object.text
        response_data['note_created_date'] = note_object.created_date.strftime('%Y-%m-%d %H:%M')

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required(login_url='/login/')
def add_notification(request):
    if request.method == 'POST':
        lead_id = request.POST.get('lead_id')
        notification_data = request.POST.get('notification_data')
        time = models.parse_datetime(request.POST.get('time'))
        manager = request.user
        response_data = {}

        notification_object = models.Notification(lead_id=lead_id, text=notification_data, time=time, manager=manager)
        notification_object.save()

        response_data['result'] = 'Create notification successful!'
        response_data['notification_text'] = notification_object.text
        response_data['notification_time'] = notification_object.time.strftime('%Y-%m-%d %H:%M')

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required(login_url='/login/')
def update_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        task = models.Task.objects.get(pk=task_id)
        task.complete = True
        task.save()

        response_data = {'result': 'Update task successful!'}

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required(login_url='/login/')
def add_task(request):
    if request.method == 'POST':
        manager = models.User.objects.get(id=request.POST.get('manager'))
        text = request.POST.get('text')
        expiration_time = models.parse_datetime(request.POST.get('expiration_time'))

        task = models.Task(manager=manager, text=text, expiration_time=expiration_time, type='t')
        task.save()

        response_data = {'result': 'Create task successful!'}

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
