import mimetypes, hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from ..models import Patient, DocumentReference
from ..forms import DocumentUploadForm
from ..services.ocr import extract_text_from_file


def document_list(request):
    docs = DocumentReference.objects.filter(patient__owner=request.user).select_related("patient")
    return render(request, "emr/documents_list.html", {"documents": docs})


def document_upload(request):
    # requires ?patient=<id> in query or select in form (for simplicity use query param)
    patient_id = request.GET.get("patient")
    patient = None
    if patient_id:
        try:
            patient = Patient.objects.get(pk=patient_id, owner=request.user)
        except Patient.DoesNotExist:
            patient = None

    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            # ensure patient selected
            pid = request.POST.get("patient_id") or patient_id
            if not pid:
                return render(request, "emr/document_upload.html", {"form": form, "error": "Select a patient."})
            patient = Patient.objects.get(pk=pid, owner=request.user)
            doc.patient = patient

            # metadata
            f = request.FILES.get("file")
            doc.size_bytes = f.size
            doc.mime = f.content_type or (mimetypes.guess_type(f.name)[0] or "")
            doc.save()

            # OCR/Extract (stub)
            text = extract_text_from_file(doc.file.path, mime=doc.mime)
            if text:
                doc.text_cache = text[:50000]  # limit
                doc.save(update_fields=["text_cache"])

            return redirect("emr:document_detail", pk=doc.pk)
    else:
        form = DocumentUploadForm()

    return render(request, "emr/document_upload.html", {"form": form, "patient": patient})


def document_detail(request, pk):
    doc = get_object_or_404(DocumentReference, pk=pk, patient__owner=request.user)
    return render(request, "emr/document_detail.html", {"doc": doc})
