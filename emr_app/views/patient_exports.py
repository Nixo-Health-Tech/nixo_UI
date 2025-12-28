from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone

from ..models import (
    Patient, Condition, MedicationStatement, AllergyIntolerance,
    Immunization, VitalSign, Observation, DiagnosticReport, DocumentReference
)

def _collect_context(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id, owner=request.user)
    ctx = {
        "now": timezone.now(),
        "patient": patient,
        "problems": Condition.objects.filter(patient=patient, status="active").order_by("description"),
        "meds": MedicationStatement.objects.filter(patient=patient, status="active").select_related("medication"),
        "allergies": AllergyIntolerance.objects.filter(patient=patient, status="active"),
        "immunizations": Immunization.objects.filter(patient=patient).order_by("-date")[:20],
        "vitals": VitalSign.objects.filter(patient=patient).order_by("-datetime")[:10],
        "recent_observations": Observation.objects.filter(patient=patient).order_by("-datetime")[:20],
        "reports": DiagnosticReport.objects.filter(patient=patient).order_by("-datetime")[:10],
        "documents": DocumentReference.objects.filter(patient=patient).order_by("-uploaded_at")[:25],
    }
    return ctx

def cpp_print_view(request, patient_id):
    ctx = _collect_context(request, patient_id)
    return render(request, "emr/cpp_print.html", ctx)

def patient_packet_view(request, patient_id):
    ctx = _collect_context(request, patient_id)
    return render(request, "emr/patient_packet.html", ctx)

def patient_packet_pdf_view(request, patient_id):
    ctx = _collect_context(request, patient_id)
    # Try WeasyPrint; fall back to HTML if unavailable
    try:
        from weasyprint import HTML
        html = render_to_string("emr/patient_packet.html", ctx, request=request)
        pdf_bytes = HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()
        resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        resp['Content-Disposition'] = f'attachment; filename="patient_{patient_id}_packet.pdf"'
        return resp
    except Exception as e:
        # Fallback: plain HTML
        return render(request, "emr/patient_packet.html", ctx)
