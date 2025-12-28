from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Patient, DocumentReference, Observation, Condition, MedicationStatement, AllergyIntolerance
from ..forms import PatientForm


def patient_list(request):
    patients = Patient.objects.filter(owner=request.user).order_by("full_name")
    return render(request, "emr/patient_list.html", {"patients": patients})

def patient_create(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.owner = request.user
            p.save()
            return redirect("emr:patient_detail", pk=p.pk)
    else:
        form = PatientForm()
    return render(request, "emr/patient_form.html", {"form": form})


def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk, owner=request.user)
    docs = DocumentReference.objects.filter(patient=patient)[:10]
    labs = Observation.objects.filter(patient=patient)[:10]
    problems = Condition.objects.filter(patient=patient)
    meds = MedicationStatement.objects.filter(patient=patient)
    allergies = AllergyIntolerance.objects.filter(patient=patient)
    return render(request, "emr/patient_detail.html", {
        "patient": patient,
        "documents": docs,
        "observations": labs,
        "problems": problems,
        "meds": meds,
        "allergies": allergies,
    })
