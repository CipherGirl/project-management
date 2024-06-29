from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Projects

# Create your views here.
# def home(request):
    # return render(request, 'projects/home.html')

class ProjectList(LoginRequiredMixin, ListView):
    model = Projects
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'
    # ordering = ['complete']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = context['projects'].filter(user=self.request.user)
        context['count'] = context['projects'].filter(complete=False).count()

        return context

class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Projects
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'

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
    