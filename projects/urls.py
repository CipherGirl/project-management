from django.urls import path
from .views import (
    ProjectList,
    ProjectDetail,
    ProjectCreate,
    ProjectUpdate,
    ProjectDelete,
    UserLoginView,
    RegisterPage,
    TaskList,
    TaskDetail,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", ProjectList.as_view(), name="project_list"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", RegisterPage.as_view(), name="register"),
    path("project/<int:pk>/", ProjectDetail.as_view(), name="project_detail"),
    path("project/create/", ProjectCreate.as_view(), name="project_create"),
    path("project/update/<int:pk>", ProjectUpdate.as_view(), name="project_update"),
    path("project/delete/<int:pk>", ProjectDelete.as_view(), name="project_delete"),
    # Task URLs
    path("project/<int:pk>/tasks/", TaskList.as_view(), name="task_list"),
    path(
        "project/<int:pk>/task/<int:task_pk>/", TaskDetail.as_view(), name="task_detail"
    ),
    path("project/<int:pk>/task/create/", TaskCreate.as_view(), name="task_create"),
    path(
        "project/<int:pk>/task/update/<int:task_pk>/",
        TaskUpdate.as_view(),
        name="task_update",
    ),
    path(
        "project/<int:pk>/task/delete/<int:task_pk>/",
        TaskDelete.as_view(),
        name="task_delete",
    ),
]
