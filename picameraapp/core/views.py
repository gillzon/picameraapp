from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import views
from django.contrib.auth.models import User
from django.views.generic import (CreateView, 
                                    UpdateView, 
                                    DeleteView, 
                                    DetailView, 
                                    TemplateView, 
                                    ListView, 
                                    View, 
                                    FormView)
from time import sleep

# Create your views her





class LoggedIn(TemplateView):
    template_name = 'login_index.html'