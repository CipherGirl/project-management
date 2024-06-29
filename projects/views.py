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
        for task in tasks:
            print(task.assigned_to)
        return context

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Projects
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('project_list')
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user = self.request.user  # Set the project owner
        project.save()
        project.members.add(self.request.user)  # Add the owner as a member
        return super(ProjectCreate, self).form_valid(form)

class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Projects
    fields = ['title', 'description', 'complete']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()

        # Add the current user to project members if not already a member
        if self.request.user not in project.members.all():
            project.members.add(self.request.user)
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['members'] = project.members.all()
        context['all_users'] = User.objects.exclude(id=project.user.id)
        return context

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        members = request.POST.getlist('members')  # Get list of selected member IDs from form

        # Clear existing members and add selected members
        project.members.clear()
        for member_id in members:
            user = get_object_or_404(User, id=member_id)
            project.members.add(user)

        return super().post(request, *args, **kwargs)

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
    
    orphaned_tasks = Task.objects.filter(project__isnull=True)
    orphaned_tasks.delete()

    def get_queryset(self):
        project = get_object_or_404(Projects, id=self.kwargs['pk'])
        return Task.objects.filter(project=project)

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'
    

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'status']
    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        project = get_object_or_404(Projects, id=self.kwargs['pk'])
        form.instance.project = project
        assigned_to_id = self.request.POST.get('assigned_to')
        if assigned_to_id:
            form.instance.assigned_to = User.objects.get(id=assigned_to_id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Projects, id=self.kwargs['pk'])
        context['project'] = project
        context['users'] = project.members.all()  # Provide project members for the dropdown
        return context

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['pk']})

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'status']
    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        assigned_to_id = self.request.POST.get('assigned_to')  # Get selected assignee ID from POST data
        if assigned_to_id:
            form.instance.assigned_to = User.objects.get(id=assigned_to_id)
        else:
            form.instance.assigned_to = None  # Clear the assignee if none is selected
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        project = task.project  # Use the task's existing project
        context['project'] = project
        context['users'] = project.members.all()  # Provide project members for the dropdown
        return context

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})

