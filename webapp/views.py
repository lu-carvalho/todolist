from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.list import ListView

from .models import *

# ---------------------- #
#          Form          #
# ---------------------- #

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["user"]
        widgets = {"description": forms.Textarea(attrs={"placeholder": "Description", "rows": 1})}

# ---------------------- #
#          Views         #
# ---------------------- # 

def index(request):
    if request.user.is_authenticated:

        user = User.objects.get(id=request.user.id)
        tasks = Task.objects.filter(user=user)

        return render(request, "webapp/index.html", {
            "tasks": tasks,
            "add_taskForm": TaskForm()
        })
    
    # if user is not authenticated, redirect to the login page
    return HttpResponseRedirect(reverse("login"))

@login_required
def add_task(request):

    # Handles logic to add new task, only takes POST method #
    form = TaskForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            complete = form.cleaned_data["complete"]

            task = Task(
                user=User.objects.get(id=request.user.id),
                title = title,
                description = description,
                complete = complete
            )
            task.save()
    return HttpResponseRedirect(reverse("login"))

def register(request):
    # for the register view, I need an html very similar to the login one, that receives a "message" variable
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Demand password and password confirmation. Ensure they match. 
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "webapp/register.html", {
                "message": "Password and confirmation must match"
            })
        
        # IntegrityError: Django's exception raised when the relational integrity of the database is affected, e.g. duplicate key. Avoid equal usernames.
        try: 
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "webapp/register.html", {
                "message": "Sorry, mate. This username is so good it is already taken. Try another!"
            })

        # If the registering works, take user to index page.
        login(request, user) 
        return(HttpResponseRedirect(reverse("index")))

    else:
        return render(request, "webapp/register.html")

def login_view(request):

    #if the user is already logged in, redirect to index page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        
        # Authenticate the user
        username = request.POST["username"]
        password = request.POST["password"]
        # If credentias are valid, the authenticate function will return an User object
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "webapp/login.html", {
                "message": "Sorry, mate. Either this isn't you or you don't have an account."
            })
    else:
        return render(request, "webapp/login.html")
 
@login_required
def task_view(request, task_id):
    
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return render(request, "webapp/error.html", { 
            "code": 404,
            "message": "That's not a task... Yet!"
        })

    if request.user.id != task.user.id:
        return render(request, "webapp/error.html", {
            "code": 404,
            "message": "That's not a task... Yet!"
        })     

    form = TaskForm(instance = task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance = task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))

    else: 
        return render(request, "webapp/task_view.html", {
            "task": task,
            "form": form
        })

@login_required
def delete_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return render(request, "webapp/error.html", { 
            "code": 404,
            "message": "That's not a task... Yet!"
        })

    if request.user.id != task.user.id:
        return render(request, "webapp/error.html", {
            "code": 404,
            "message": "That's not a task... Yet!"
        })

    task.delete()
    return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))