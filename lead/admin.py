from django.contrib import admin

from .models import Lead

admin.site.register(Lead)

admin.site.site_header = 'BKT'