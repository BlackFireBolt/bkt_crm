from .models import Notification


def lead_context_processor(request):
    context = { 'events': Notification.objects.all() }
    return context