from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AIModelTool, ModelRun, RunStatus
from .forms import ImagingRunForm
from .services import run_cxr


def tools_catalog(request):
    tools = AIModelTool.objects.filter(active=True)
    return render(request, "ai_models/catalog.html", {"tools": tools})


def run_create(request, slug):
    tool = get_object_or_404(AIModelTool, slug=slug, active=True)
    if tool.type != "image":
        return redirect("ai_models:catalog")

    patient_id = request.GET.get("patient")  # optional
    if request.method == "POST":
        form = ImagingRunForm(request.POST, request.FILES)
        if form.is_valid():
            run = form.save(commit=False)
            run.owner = request.user
            run.tool = tool
            pid = form.cleaned_data.get("patient_id") or patient_id
            if pid:
                from emr_app.models import Patient
                run.patient = get_object_or_404(Patient, pk=pid, owner=request.user)
            run.status = RunStatus.PENDING
            run.save()
            return redirect("ai_models:run_detail", pk=run.pk)
    else:
        form = ImagingRunForm(initial={"patient_id": patient_id or ""})

    return render(request, "ai_models/run_create.html", {"tool": tool, "form": form})


def run_detail(request, pk):
    run = get_object_or_404(ModelRun, pk=pk, owner=request.user)
    return render(request, "ai_models/run_detail.html", {"run": run})


def run_execute(request, pk):
    run = get_object_or_404(ModelRun, pk=pk, owner=request.user)
    if run.tool.slug == "cxr":
        run_cxr(run)   # synchronous; می‌توانید بعدها Celery کنید
    # future: elif run.tool.slug == "breast_cancer": ...
    return redirect("ai_models:run_detail", pk=pk)
