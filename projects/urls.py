from django.urls import path
from .views import ProjectList, ProjectDetail, ProjectCreate, ProjectUpdate, ProjectDelete, UserLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', ProjectList.as_view(), name='project_list'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('project/<int:pk>/', ProjectDetail.as_view(), name='project_detail'),
    path('project-create/', ProjectCreate.as_view(), name='project_create'),
    path('project-update/<int:pk>', ProjectUpdate.as_view(), name='project_update'),
    path('project-delete/<int:pk>', ProjectDelete.as_view(), name='project_delete'),
    # path('', views.project_list, name='project_list'),
    # path('project/new/', views.project_create, name='project_create'),
    # path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    # path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
]