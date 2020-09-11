from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from .views import LeadListView, LeadListViewAdmin, lead_detail
from .views import add_lead, change_lead, add_lead_post

app_name = 'lead'
urlpatterns = [
    path('change-lead/', change_lead, name='change-lead'),
    path('add-lead-post/', add_lead, name='add-lead-post'),
    path('add-lead/', add_lead, name='add-lead'),
    path('detail/<int:pk>', lead_detail, name='lead-detail'),
    path('admin_page/', LeadListViewAdmin.as_view(), name='admin-index'),
    path('', LeadListView.as_view(), name='index'),
]
