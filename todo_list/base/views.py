from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Task


class TaskList(ListView):
    model = Task
    context_object_name = 'task'


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
