from .models import Notification, Task
from .forms import TaskForm


def lead_context_processor(request):
    context = {'events': Notification.objects.filter(manager=request.user.id),
               'task_form': TaskForm()}
    if request.user.groups.filter(name='Администратор').exists():
        context['tasks'] = Task.objects.all()
    else:
        context['tasks'] = Task.objects.filter(manager=request.user.id)
    return context