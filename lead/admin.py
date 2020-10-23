from django.contrib import admin

from .models import Lead, Note, Notification, Task


class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'created_date', 'manager')


class NoteAdmin(admin.ModelAdmin):
    list_display = ('lead', 'created_date')


admin.site.register(Lead, LeadAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Notification)
admin.site.register(Task)

admin.site.site_header = 'BKT'