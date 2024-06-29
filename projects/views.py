from django.shortcuts import render, HttpResponse
from django.views.generic import ListView 
from .models import Projects

# Create your views here.
# def home(request):
    # return render(request, 'projects/home.html')

class ProjectListView(ListView):
    model = Projects
    # template_name = 'projects/project.html'
    # context_object_name = 'projects'
    # ordering = ['complete']