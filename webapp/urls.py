from django.urls import path

from . import views

# URL names makes it easier to reference them from other parts of the web application
urlpatterns = [
    path("", views.index,name ="index"),
    path("login", views.login_view, name="login"),
    path("task/<int:task_id>", views.task_view, name="task_view"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("task/delete/<int:task_id>", views.delete_task, name="delete_task"),
    path("add_task", views.add_task, name="add_task")
]