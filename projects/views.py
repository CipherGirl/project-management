from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Projects, Task
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.urls import resolve


# Custom view for handling PermissionDenied
def custom_permission_denied_view(request, exception):
    return render(request, "projects/403.html", status=403)


# View to list all projects the user is involved in
class ProjectList(LoginRequiredMixin, ListView):
    model = Projects
    context_object_name = "projects"
    template_name = "projects/project_list.html"

    def get_queryset(self):
        user = self.request.user
        # Fetch projects where the user is either the creator or a member
        return Projects.objects.filter(Q(created_by=user) | Q(members=user)).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = context["projects"]

        # Count incomplete projects
        count_incomplete = projects.filter(complete=False).count()

        context["count"] = count_incomplete
        return context


# View to show details of a specific project
class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Projects
    context_object_name = "project"
    template_name = "projects/project_detail.html"

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        # Check if the user is a member of the project
        if request.user not in project.members.all():
            return redirect("project_list")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        tasks = Task.objects.filter(project=project)
        context["tasks"] = tasks
        return context


# View to create a new project
class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Projects
    fields = ["title", "description", "complete"]
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("project_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Create Project"
        context["submit_button_text"] = "Create Project"
        context["all_users"] = User.objects.exclude(id=self.request.user.id)
        context["members"] = []
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.created_by = self.request.user
        project.save()

        if self.request.user not in project.members.all():
            project.members.add(self.request.user)

        selected_members_ids = self.request.POST.getlist("members")
        for member_id in selected_members_ids:
            member = User.objects.get(id=member_id)
            project.members.add(member)

        return super().form_valid(form)


# View to update an existing project
class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Projects
    fields = ["title", "description", "complete"]
    template_name = "projects/project_form.html"

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if not project.created_by == request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context["form_title"] = "Update Project"
        context["submit_button_text"] = "Update Project"
        context["members"] = project.members.all()
        context["all_users"] = User.objects.exclude(id=project.created_by.id)
        return context

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        members = request.POST.getlist("members")
        members.append(str(request.user.id))
        if not project.created_by == request.user:
            raise PermissionDenied

        current_user = request.user
        if current_user not in project.members.all():
            project.members.add(current_user)

        project.members.clear()
        for member_id in members:
            user = get_object_or_404(User, id=member_id)
            project.members.add(user)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("project_detail", kwargs={"pk": self.object.pk})


# View to delete a project
class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Projects
    context_object_name = "project"
    success_url = reverse_lazy("project_list")
    template_name = "projects/project_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user != project.created_by:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# View to handle user login
class UserLoginView(LoginView):
    template_name = "projects/login.html"
    fields = "__all__"
    redirect_authenticated_user = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_view"] = resolve(self.request.path_info).url_name
        return context

    def get_success_url(self):
        return (
            reverse_lazy("project_list")
            if self.request.user.is_authenticated
            else reverse_lazy("login")
        )


# View to handle user registration
class RegisterPage(FormView):
    template_name = "projects/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("project_list")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_view"] = resolve(self.request.path_info).url_name
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("project_list")
        return super().get(*args, **kwargs)


# View to list all tasks in a project
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"

    def get_queryset(self):
        project = get_object_or_404(Projects, id=self.kwargs["pk"])
        return Task.objects.filter(project=project)


# View to show details of a specific task
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"


# View to create a new task
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "status"]
    template_name = "tasks/task_form.html"

    def form_valid(self, form):
        project = get_object_or_404(Projects, id=self.kwargs["pk"])
        form.instance.project = project
        assigned_to_id = self.request.POST.get("assigned_to")
        if assigned_to_id:
            form.instance.assigned_to = User.objects.get(id=assigned_to_id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Projects, id=self.kwargs["pk"])
        context["project"] = project
        context["users"] = project.members.all()
        return context

    def get_success_url(self):
        return reverse_lazy("project_detail", kwargs={"pk": self.kwargs["pk"]})


# View to update an existing task
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "status"]
    template_name = "tasks/task_form.html"

    def get_object(self, queryset=None):
        project = get_object_or_404(Projects, id=self.kwargs["pk"])
        task = get_object_or_404(Task, id=self.kwargs["task_pk"], project=project)

        if self.request.user not in project.members.all():
            raise PermissionDenied
        return task

    def form_valid(self, form):
        assigned_to_id = self.request.POST.get("assigned_to")
        if assigned_to_id:
            form.instance.assigned_to = User.objects.get(id=assigned_to_id)
        else:
            form.instance.assigned_to = None
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        project = task.project
        context["project"] = project
        context["users"] = project.members.all()
        return context

    def get_success_url(self):
        return reverse_lazy("project_detail", kwargs={"pk": self.object.project.id})


# View to delete a task
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task_confirm_delete.html"

    def get_object(self, queryset=None):
        project = get_object_or_404(Projects, id=self.kwargs["pk"])
        task = get_object_or_404(Task, id=self.kwargs["task_pk"], project=project)

        if self.request.user not in project.members.all():
            raise PermissionDenied
        return task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        project = task.project
        context["project"] = project
        return context

    def get_success_url(self):
        return reverse_lazy("project_detail", kwargs={"pk": self.object.project.id})
