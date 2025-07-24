from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Task
from .Forms import TaskForm
# Create your views here.


def home(request):
    return render(request, "home.html")


def signUp(request):
    if request.method == "GET":
        return render(request, "signup.html")
    else:
        if request.POST["password1"] == request.POST["password2"]:
            # Registro de usuario
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, "signup.html", {
                    "error": "El usuario ya existe"
                })
        else:
            return render(request, "signup.html",
                          {"error": "Passwords no coinciden"})


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html", {
            "form": AuthenticationForm()
        })
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, "login.html", {
                "form": AuthenticationForm(),
                "error": "Usuario o contraseña incorrectos"
            })
        else:
            login(request, user)
            return redirect("tasks")


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks.html", {"tasks": tasks})


@login_required
def createTask(request):
    if request.method == "GET":
        form = TaskForm()
        return render(request, "taskform.html", {"form": form})
    else:
        try:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect("tasks")
            else:
                return render(request, "taskform.html", {"form": form, "error": "Formulario inválido"})
        except ValueError:
            return render(request, "taskform.html", {"form": TaskForm(), "error": "Error al crear la tarea"})


@login_required
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.delete()
        return redirect("tasks")
    except Task.DoesNotExist:
        return HttpResponse("Tarea no encontrada o no tienes permiso para eliminarla.")


@login_required
def edit_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        if request.method == "GET":
            form = TaskForm(instance=task)
            return render(request, "taskform.html", {"form": form})
        else:
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect("tasks")
            else:
                return render(request, "taskform.html", {"form": form, "error": "Formulario inválido"})
    except Task.DoesNotExist:
        return HttpResponse("Tarea no encontrada o no tienes permiso para editarla.")


@login_required
def cerrarSesion(request):
    logout(request)
    return redirect("home")
