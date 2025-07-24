from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signUp, name="signup"),
    path("logout/", views.cerrarSesion, name="logout"),
    path("login/", views.login_view, name="login"),
    path("tasks/", views.tasks, name="tasks"),
    path("taskform/", views.createTask, name="taskform"),
    path("delete_task/<int:task_id>/", views.delete_task, name="delete_task"),
    path("taskform/<int:task_id>/", views.edit_task, name="taskform_edit"),
]
