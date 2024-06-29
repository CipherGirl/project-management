from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView  
from django.urls import reverse_lazy
from .models import Projects

# Create your views here.
# def home(request):
    # return render(request, 'projects/home.html')

class ProjectListView(ListView):
    model = Projects
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'
    # ordering = ['complete']

class ProjectDetail(DetailView):
    model = Projects
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'

class ProjectCreate(CreateView):
    model = Projects
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('project_list')
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ProjectUpdate(UpdateView):
    model = Projects
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('project_list')
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)