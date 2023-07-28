from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task'] = context['task'].filter(title__icontains=search_input)
            context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('base:task')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('base:task')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('base:task')


class UserLogin(LoginView):
    template_name = "base/login.html"
    fields = ['title', 'description', 'complete']
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('base:task')


class RegisterPage(FormView):
    template_name = "base/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('base:task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)

        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('base:task')
        return super(RegisterPage, self).get(*args, **kwargs)


