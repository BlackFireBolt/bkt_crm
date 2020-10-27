from django.contrib import admin
import csv, datetime
from django.http import HttpResponse

from .models import Lead, Note, Notification, Task


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' \
                                      'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Экспорт в CSV'


class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'created_date', 'manager')
    actions = [export_to_csv]


class NoteAdmin(admin.ModelAdmin):
    list_display = ('lead', 'created_date')


admin.site.register(Lead, LeadAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Notification)
admin.site.register(Task)

admin.site.site_header = 'BKT'