# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view
from django.contrib.auth.views import LogoutView

app_name = 'authentication'
urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', LogoutView.as_view(), name="logout")
]
