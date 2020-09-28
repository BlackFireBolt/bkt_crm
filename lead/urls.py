from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from . import views

app_name = 'lead'
urlpatterns = [
    path('admin_page_json/', views.AdminListLeadJson.as_view(), name='admin_lead_list_json'),
    path('admin_page/', views.AdminListLead.as_view(), name='admin_lead_list'),
    path('change-lead/', views.change_lead, name='change-lead'),
    path('add-lead-post/', views.add_lead_post, name='add-lead-post'),
    path('add-lead/', views.add_lead, name='add-lead'),
    path('detail/<int:pk>', views.lead_detail, name='lead-detail'),
    #path('admin_page/', LeadListViewAdmin.as_view(), name='admin-index'),
    path('index_json/', views.ListLeadJson.as_view(), name='lead_list_json'),
    path('', views.ListLead.as_view(), name='index'),
]
