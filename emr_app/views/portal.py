# emr_app/views/portal.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.http import Http404
from django.db.models import Q

from ..utils import get_model, field_names, has_field, get_or_create_self_patient
from django.urls import reverse

def entry(request):
    if not request.user.is_authenticated:
        return redirect(f"{reverse('login:login')}?next={reverse('emr:my_dashboard')}")
    # دیگر بررسی role/staff نمی‌کنیم؛ همه مستقیم به پرتال شخصی
    return redirect('emr:my_dashboard')


def my_dashboard(request):
    patient = get_or_create_self_patient(request.user)
    # خلاصه‌های سبک (اختیاری)
    Document = None
    Observation = None
    try:
        Document = get_model("emr_app", "Document")
    except Exception:
        pass
    try:
        Observation = get_model("emr_app", "Observation")
    except Exception:
        pass

    docs = Document.objects.filter(patient=patient).order_by("-created_at")[:5] if Document else []
    obs  = Observation.objects.filter(patient=patient).order_by("-datetime")[:5] if Observation else []

    return render(request, "emr/portal/dashboard.html", {
        "patient": patient, "recent_docs": docs, "recent_observations": obs
    })


def my_profile_edit(request):
    patient = get_or_create_self_patient(request.user)
    Patient = patient.__class__
    # فیلدهای پرکاربرد—فقط آنهایی که واقعاً در مدل موجودند را استفاده کن
    candidate_fields = ["full_name", "identifier", "dob", "sex", "height_cm", "weight_kg",
                        "phone", "email", "address", "blood_group", "marital_status"]
    fields = [f for f in candidate_fields if has_field(Patient, f)]
    if not fields:
        # اگر هیچ فیلدی از بالا نبود، همه فیلدهای قابل‌ویرایش را انتخاب کن (بجز کلیدها و سیستمی‌ها)
        blacklist = {"id", "pk", "owner", "user", "created_at", "updated_at"}
        fields = [f for f in field_names(Patient) if f not in blacklist]

    Form = modelform_factory(Patient, fields=fields)

    if request.method == "POST":
        form = Form(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("emr:my_dashboard")
    else:
        form = Form(instance=patient)

    return render(request, "emr/portal/profile_form.html", {"form": form, "patient": patient})



def my_documents(request):
    patient = get_or_create_self_patient(request.user)
    try:
        Document = get_model("emr_app", "Document")
    except Exception:
        raise Http404("مدل Document یافت نشد.")

    # فرم آپلود—فیلدهای متداول: title, file, category, notes
    candidate = ["title", "file", "category", "notes"]
    fields = [f for f in candidate if has_field(Document, f)]
    if "patient" in field_names(Document):
        fields_plus = [f for f in fields if f != "patient"]
    else:
        fields_plus = fields
    Form = modelform_factory(Document, fields=fields_plus)

    if request.method == "POST":
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            # اتصال به بیمار
            if has_field(Document, "patient"):
                obj.patient = patient
            elif has_field(Document, "subject"):
                obj.subject = patient
            obj.save()
            return redirect("emr:my_documents")
    else:
        form = Form()

    docs = Document.objects.all()
    # محدود به بیمار جاری
    if has_field(Document, "patient"):
        docs = docs.filter(patient=patient)
    elif has_field(Document, "subject"):
        docs = docs.filter(subject=patient)

    return render(request, "emr/portal/documents.html", {"form": form, "documents": docs})



def my_observations(request):
    patient = get_or_create_self_patient(request.user)
    try:
        Observation = get_model("emr_app", "Observation")
    except Exception:
        raise Http404("مدل Observation یافت نشد.")

    # فیلدهای متداول: code (نوع مشاهده)، value, unit, datetime, notes
    candidate = ["code", "value", "unit", "datetime", "notes"]
    fields = [f for f in candidate if has_field(Observation, f)]
    Form = modelform_factory(Observation, fields=fields)

    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            # اتصال به بیمار
            if has_field(Observation, "patient"):
                obj.patient = patient
            elif has_field(Observation, "subject"):
                obj.subject = patient
            obj.save()
            return redirect("emr:my_observations")
    else:
        form = Form()

    obs = Observation.objects.all()
    if has_field(Observation, "patient"):
        obs = obs.filter(patient=patient)
    elif has_field(Observation, "subject"):
        obs = obs.filter(subject=patient)

    return render(request, "emr/portal/observations.html", {"form": form, "observations": obs})


def legacy_patients_redirect(request):
    return redirect('emr:my_dashboard')