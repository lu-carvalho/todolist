from django.contrib.auth.models import AbstractUser
from django.db import models

# I will need a User model and a Task model 
# See on Django's documentation what exactly is AbstractUser

class User(AbstractUser):
    pass

class Task(models.Model):
    # task needs a title
    # a description
    # a complete or not complete logic
    pass
