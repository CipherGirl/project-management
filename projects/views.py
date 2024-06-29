from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Projects, Task

# Project views ...

class ProjectList(LoginRequiredMixin, ListView):
    model = Projects
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = context['projects'].filter(user=self.request.user)
        context['count'] = context['projects'].filter(complete=False).count()
        return context

class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Projects
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        tasks = Task.objects.filter(project=project)
        context['tasks'] = tasks
        return context

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Projects
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('project_list')
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProjectCreate, self).form_valid(form)

class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Projects
    fields =  ['title', 'description', 'complete']
    success_url = reverse_lazy('project_list')
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Projects
    context_object_name = 'project'
    success_url = reverse_lazy('project_list')
    template_name = 'projects/project_confirm_delete.html'

class UserLoginView(LoginView):
    template_name = 'projects/login.html'
    fields = '__all__'
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('project_list') if self.request.user.is_authenticated else reverse_lazy('login')

class RegisterPage(FormView):
    template_name = 'projects/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated: 
            return redirect('project_list')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        project = get_object_or_404(Projects, id=self.kwargs['pk'])
        return Task.objects.filter(project=project)

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'status']  # Include 'assigned_to' if not using the default User model

    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        print(self.request.POST) 
        project = get_object_or_404(Projects, id=self.kwargs['pk'])
        form.instance.project = project
        form.instance.user = self.request.user  # Assign current user
        assigned_to_id = self.request.POST.get('assigned_to')  # Get selected assignee ID from POST data
        if assigned_to_id:
            form.instance.assigned_to = User.objects.get(id=assigned_to_id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Projects, id=self.kwargs['pk'])
        context['users'] = User.objects.all()  # Provide all users for the dropdown
        return context

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['pk']})
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'status']
    template_name = 'tasks/task_form.html'

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})

