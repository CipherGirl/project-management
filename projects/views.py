from django.shortcuts import render, HttpResponse
from django.views.generic import ListView 
from django.views.generic import DetailView 
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
