from django.urls import path
from .views import patients, documents, observations, clinical,patient_exports
from .views import portal as portal_views
app_name = "emr"

urlpatterns = [


    path("", portal_views.entry, name="entry"),

    # پرتال شخصی
    path("my/", portal_views.my_dashboard, name="my_dashboard"),
    path("my/profile/", portal_views.my_profile_edit, name="my_profile"),
    path("my/documents/", portal_views.my_documents, name="my_documents"),
    path("my/observations/", portal_views.my_observations, name="my_observations"),

    # لینک‌های قدیمی — همه به پرتال شخصی بروند
    path("patients/", portal_views.legacy_patients_redirect, name="patients_legacy"),

    path("documents/", documents.document_list, name="document_list"),
    path("documents/upload/", documents.document_upload, name="document_upload"),
    path("documents/<int:pk>/", documents.document_detail, name="document_detail"),

    path("patients/<int:patient_id>/cpp/print/", patient_exports.cpp_print_view, name="cpp_print"),
    path("patients/<int:patient_id>/packet/", patient_exports.patient_packet_view, name="patient_packet"),
    path("patients/<int:patient_id>/packet/pdf/", patient_exports.patient_packet_pdf_view, name="patient_packet_pdf"),

    path("labs/", observations.observations_list, name="observations_list"),
]
