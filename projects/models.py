from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='projects', blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete']

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    title = models.CharField(max_length=200)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned', null=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['status', 'created']
