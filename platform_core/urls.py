from django.urls import path
from . import views

app_name = "tools"
urlpatterns = [
    path("", views.tool_list, name="list"),
    path("<slug:slug>/", views.tool_detail, name="detail"),
    path("<slug:slug>/run/", views.run_tool, name="run"),
    path("executions/<int:pk>/", views.execution_detail, name="execution_detail"),
]
