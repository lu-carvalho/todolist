from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import froms
from django.core.exceptions import ObjectDoesNotExist

from .models import *

# I will need a login page, which contains only the login form
# Also needs a register page
# The logout page will redirect me to the login page
# After loging in, the user will have only one view: the main view of his to-do list
# It must contain a logout rediret button 
# it will be compound of a rectangule (?) on the midle (g luck centering this div haha), in which he can: 
# 1) add new tasks
    # form is needed. 
# 2) view the tasks
# 3) if the task is marked as complete, it will turn green, fade, italic and crossed
# 4) edit the task
# 5) delete the task
# 6) if all tasks are complete: think of a happy face or something like that 
# maybe implement some other features like adding time to be spent on each task, smthg like that
# for my models, I only will need the User one, that is provided by Django and a task model

# # # # # # # # # 
#     FORMS     #
# # # # # # # # # 


# # # # # # # # # 
#     VIEWS     #
# # # # # # # # # 

#TO BE DONE
def index(request):
    pass

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

        # If the registering works, take user to login page. 
        return(HttpResponseRedirect(reverse("login")))

    else:
        return render(request, "webapp/register.html")

def login_view(request):
    # for the login view I have to create an login.html template that displays the authentication form and accepts a message (Remember to add the "if empty" in case there is no message)
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
            return render(request, "todolist/login.html", {
                "message": "Sorry, mate. Either this isn't you or you don't have an account."
            })
    else:
        return render(request, "todolist/login.html")
    
@login_required
def logout_view(request):
    # Logically, login is required to logout 
    logout(request)
    return HttpResponseRedirect(reverse("index"))