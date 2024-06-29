from django.urls import path
from .views import ProjectListView

urlpatterns = [
    path('', ProjectListView.as_view(), name='projects'),
    # path('', views.project_list, name='project_list'),
    # path('project/<int:pk>/', views.project_detail, name='project_detail'),
    # path('project/new/', views.project_create, name='project_create'),
    # path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    # path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
]