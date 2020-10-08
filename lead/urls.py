from django.urls import path

from . import views

app_name = 'lead'
urlpatterns = [
    path('admin_page_json/', views.AdminListLeadJson.as_view(), name='admin_lead_list_json'),
    path('admin_page/', views.AdminListLead.as_view(), name='admin_lead_list'),
    path('add_manager/', views.add_manager, name='add-manager'),
    path('import_csv/', views.add_import, name='add-import'),
    path('change-lead/', views.change_lead, name='change-lead'),
    path('add-lead-post/', views.add_lead_post, name='add-lead-post'),
    path('add-lead/', views.add_lead, name='add-lead'),
    path('add-note/', views.add_note, name='add-note'),
    path('detail/<int:pk>', views.lead_detail, name='lead-detail'),
    path('index_json/', views.ListLeadJson.as_view(), name='lead_list_json'),
    path('', views.ListLead.as_view(), name='index'),
]
