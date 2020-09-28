from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_tables2 import SingleTableView, LazyPaginator
from django.views.decorators.csrf import csrf_exempt
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import TemplateView

from .models import Lead
from .tables import LeadTable, LeadTableAdmin
from .forms import LeadForm
from braces.views import GroupRequiredMixin


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


@login_required(login_url='/login/')
def add_lead(request):
    pass


@login_required(login_url='/login/')
def change_lead(request):
    if request.method == 'POST':
        pass
