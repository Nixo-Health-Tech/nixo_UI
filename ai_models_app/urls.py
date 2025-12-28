from django.urls import path
from . import views

app_name = "ai_models"
urlpatterns = [
    path("", views.tools_catalog, name="catalog"),
    path("run/<slug:slug>/new/", views.run_create, name="run_create"),
    path("runs/<int:pk>/", views.run_detail, name="run_detail"),
    path("runs/<int:pk>/run/", views.run_execute, name="run_execute"),
]
