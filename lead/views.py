from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_tables2 import SingleTableView, LazyPaginator
from django.views.decorators.csrf import csrf_exempt
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import TemplateView
import json, csv, phonenumbers
from phonenumbers import timezone

from .models import Lead, User
from .tables import LeadTable, LeadTableAdmin
from .forms import LeadForm, ImportForm, LeadManagerForm
from braces.views import GroupRequiredMixin


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


class LeadListView(LoginRequiredMixin, SingleTableView):
    model = Lead
    table_class = LeadTable
    paginator_class = LazyPaginator
    template_name = 'lead_list.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        context['form'] = LeadForm()
        return context


class ListLeadJson(LoginRequiredMixin, BaseDatatableView):
    model = Lead
    login_url = '/login/'

    columns = ['id', 'name', 'email', 'phone', 'country', 'created_date', 'status']

    def get_initial_queryset(self):
        return Lead.objects.exclude(status='d').filter(manager=self.request.user.id)


class ListLead(LoginRequiredMixin, TemplateView):
    template_name = 'lead_list.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(ListLead, self).get_context_data(**kwargs)
        context['form'] = LeadForm()
        return context


class AdminListLeadJson(GroupRequiredMixin, BaseDatatableView):
    model = Lead
    login_url = '/login/'
    group_required = [u'Администратор', u'admin']

    def get_initial_queryset(self):
        return Lead.objects.exclude(status='d')


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


class LeadListViewAdmin(GroupRequiredMixin, SingleTableView):
    model = Lead
    table_class = LeadTableAdmin
    paginator_class = LazyPaginator
    template_name = 'lead_list_admin.html'
    login_url = '/login/'
    group_required = [u'Администратор', u'admin']

    def get_context_data(self, **kwargs):
        context = super(LeadListViewAdmin, self).get_context_data(**kwargs)
        context['form'] = LeadForm()
        return context


@login_required(login_url='/login/')
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    lead_form = LeadForm(instance=lead)
    context = {'lead': lead, 'lead_form': lead_form}
    return render(request, 'lead_detail.html', context)


@csrf_exempt
def add_lead_post(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        country = request.POST.get('country')
        created_date = request.POST.get('created_date')

        lead = Lead(name=name, phone=phone, email=email, country=country, created_date=created_date)
        lead.save()
        return HttpResponse(status=200)


@login_required(login_url='/login/')
def add_lead(request):
    if request.method == 'POST':
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

        lead = Lead(name=name, phone=phone, email=email, country=country, time_zone=time_zone,
                    created_date=created_date, status=status, manager=User.objects.get(id=manager_id))
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
def change_lead(request):
    if request.method == 'POST':
        leadpk = request.POST.get('leadpk')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        time_zone = request.POST.get('time_zone')
        email = request.POST.get('email')
        country = request.POST.get('country')
        created_date = request.POST.get('created_date')
        notes = request.POST.get('notes')
        status = request.POST.get('status')
        manager_id = request.POST.get('manager')

        lead = Lead.objects.get(pk=leadpk)
        lead.name = name
        lead.phone = phone
        lead.email = email
        lead.country = country
        lead.created_date = created_date
        lead.notes = notes
        lead.status = status
        managerold_id = None
        if lead.manager is not None:
            managerold_id = lead.manager.id
        lead.time_zone = time_zone
        if manager_id is not None:
            lead.manager = User.objects.get(id=manager_id)
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
            phone = ''.join(filter(str.isdigit, row[int(request.POST.get('phone_field')) - 1]))
            try:
                if phonenumbers.is_valid_number(phone):
                    p = phonenumbers.parse(phone)
                    time_zone = timezone.time_zones_for_number(p)
                    country = phonenumbers.region_code_for_number(p)
            except (AttributeError, ValueError, Exception):
                pass
            lead = Lead(name=name, email=email, phone=phone, country=country, time_zone=time_zone)
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
        manager = User.objects.get(id=request.POST.get('manager'))
        for data in request.POST.getlist('data[]'):
            lead = Lead.objects.get(pk=remove_html_tags(data))
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
