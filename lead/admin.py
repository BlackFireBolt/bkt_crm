from django.contrib import admin

from .models import Lead, Note


class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'created_date', 'manager')


admin.site.register(Lead, LeadAdmin)
admin.site.register(Note)

admin.site.site_header = 'BKT'