# CRM for BKT-konsult (local project)

Django + Bootstrap 4 + PostgreSQL + Django Channels + Celery + Redis. Deployed on VPS (Nginx, Gunicorn). Managers can see information about their clients (CRUD), notifications and tasks (Celery). Admin can see all clients and all notifications and tasks in real time (Django Channels, Web Sockets). Also API for outer sources of clients (my first step in API development).


## Project setup
```
pip install -r requirements.txt
python manage.py runserver
```

WARNING! Dead project without maintenance. Some dependances issues can be posssible.