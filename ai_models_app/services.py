# ai_models_app/services.py
from __future__ import annotations
import io
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings
from .models import ModelRun, RunStatus
from .adapters import cxr as cxr_adapter

# billing (اختیاری)
try:
    from purchase_app.services import WalletService
    BILLING = True
except Exception:
    BILLING = False

# EMR (اختیاری)
try:
    from emr_app.models import DiagnosticReport
    EMR = True
except Exception:
    EMR = False

def make_llm_report(run, probs, top, lang="fa"):
    # نیاز به کتابخانه openai>=1.0
    from openai import OpenAI
    client = OpenAI()

    # کانتکست خلاصه‌شده از نتایج مدل
    top_lines = "\n".join([f"- {n}: {p:.2f}" for n, p in top]) or "یافتهٔ برجسته‌ای گزارش نشد."

    # (اختیاری) افزودن اطلاعات بیمار از EMR
    emr_ctx = ""
    try:
        if run.patient_id:
            # هر چه می‌خواهی از EMR خلاصه کن و اینجا بگذار
            emr_ctx = f"نام بیمار: {run.patient.full_name}، تاریخ تولد: {run.patient.dob}"
    except Exception:
        pass

    system = (
        "تو یک دستیار کلینیکیِ محتاط هستی. خروجی را فارسی، ساخت‌یافته و کوتاه بنویس. "
        "به‌صورت آموزشی صحبت کن و در پایان هشدار عدم‌جایگزینی با نظر پزشک را ذکر کن."
    )
    user = f"""
نتایج مدل CXR (Top findings):
{top_lines}

اطلاعات زمینه (اختیاری):
{emr_ctx}

لطفاً یک گزارش کوتاه، مرحله‌ای و قابل‌چاپ تولید کن:
- تفسیر کلی
- یافته‌های کلیدی با درصد تقریبی
- پیشنهاد پیگیری/مقایسه در صورت نیاز
- هشدار ایمنی
"""

    resp = client.chat.completions.create(
        model=getattr(settings, "REPORT_LLM_MODEL", "gpt-4o-mini"),
        messages=[{"role":"system","content":system},
                  {"role":"user","content":user}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()

def run_cxr(run: ModelRun):
    """Execute the CXR tool on a ModelRun with image."""
    tool = run.tool
    if BILLING and tool.credit_cost > 0:
        w = WalletService(run.owner)
        w.ensure_balance(tool.credit_cost)

    run.status = RunStatus.PROCESSING
    run.save(update_fields=["status"])

    try:
        img = run.image and cxr_adapter.Image.open(run.image)
        probs = cxr_adapter.predict_probs(img)
        top = cxr_adapter.top_findings(probs, k=5, th=float(getattr(settings, "CXR_REPORT_THRESHOLD", 0.3)))
        text = make_llm_report(run, probs, top)
        run.result = {"probs": probs, "top": top, "narrative": text}

        # overlay
        ov = cxr_adapter.make_overlay(img)
        buf = io.BytesIO(); ov.save(buf, format="PNG")
        run.overlay_image.save(f"overlay_{run.pk}.png", ContentFile(buf.getvalue()), save=False)

        run.result = {"probs": probs, "top": top, "narrative": text}
        run.status = RunStatus.DONE
        run.credits_charged = tool.credit_cost
        run.save()

        if BILLING and tool.credit_cost > 0:
            w.charge(tool.credit_cost, meta={"tool": tool.slug, "run_id": run.id})

        if EMR and run.patient:
            DiagnosticReport.objects.create(
                patient=run.patient,
                category="imaging",
                datetime=timezone.now(),
                title="Chest X-Ray (AI)",
                conclusion=text,
                text=str(run.result),
            )
        return run
    except Exception as e:
        run.status = RunStatus.ERROR
        run.result = {"error": str(e)}
        run.save(update_fields=["status", "result"])
        raise
