from django.urls import path

from . import views

# URL names makes it easier to reference them from other parts of the web application
urlpatterns = [
    path("", views.index,name ="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register")
]