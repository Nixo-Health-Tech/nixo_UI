from django.urls import path
from . import views

app_name = "breast"

urlpatterns = [
    # Dashboard & tools
    path("", views.dashboard, name="dashboard"),
    path("calculator/", views.risk_calculator, name="risk_calculator"),
    path("statistics/", views.assessment_statistics, name="statistics"),
    # CRUD
    path("assessments/", views.BreastCancerAssessmentListView.as_view(), name="assessment_list"),
    path("assessments/new/", views.BreastCancerAssessmentCreateView.as_view(), name="assessment_create"),
    path("assessments/<int:pk>/", views.BreastCancerAssessmentDetailView.as_view(), name="assessment_detail"),
    path("assessments/<int:pk>/edit/", views.BreastCancerAssessmentUpdateView.as_view(), name="assessment_update"),
    path("assessments/<int:pk>/delete/", views.BreastCancerAssessmentDeleteView.as_view(), name="assessment_delete"),
    path("success/", views.assessment_success, name="assessment_success"),
    # Utilities
    path("export.csv", views.export_assessments_csv, name="export_csv"),
    path("ajax/validate/", views.ajax_validate_field, name="ajax_validate"),
]
