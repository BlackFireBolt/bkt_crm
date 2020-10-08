from django.contrib import admin

from .models import Lead, Note

admin.site.register(Lead)
admin.site.register(Note)

admin.site.site_header = 'BKT'