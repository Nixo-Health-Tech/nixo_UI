from django.urls import path
from . import views

app_name = "login"

urlpatterns = [
    path("signin/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
]
