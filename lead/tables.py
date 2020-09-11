import django_tables2 as tables

from .models import Lead


class LeadTable(tables.Table):
    class Meta:
        model = Lead
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
           "data-href": lambda record: record.get_absolute_url,
            "style": lambda record: "cursor: pointer;",
        }
        fields = ("id", "status", "name", "phone", "country", "email", "created_date")


class LeadTableAdmin(LeadTable):
    class Meta(LeadTable.Meta):
        fields = ("id", "status", "name", "phone", "country", "email", "created_date", "manager")
