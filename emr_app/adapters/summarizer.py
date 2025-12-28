# EMR Summarizer adapter for your platform_core Tools runner.
# Provides a concise patient summary from existing EMR data.
try:
    from platform_core.adapters.base import BaseAdapter
except Exception:
    # fallback for standalone testing
    class BaseAdapter:
        def __init__(self, tool_spec, user, wallet_service=None):
            self.tool = tool_spec
            self.user = user
            self.wallet = wallet_service
        def input_schema(self):
            return {}
        def estimate_credits(self, input_payload): return 0
        def run(self, input_payload): return {"output": {}, "artifacts": []}

from django.utils import timezone
from emr_app.models import Patient, Condition, MedicationStatement, AllergyIntolerance, Observation, DocumentReference

class EMRSummarizer(BaseAdapter):
    def input_schema(self):
        return {
            "patient_id": {"type": "number", "required": True},
            "months": {"type": "number", "required": False, "default": 6}
        }

    def estimate_credits(self, payload): return 1

    def run(self, payload):
        pid = int(payload["patient_id"])
        months = int(payload.get("months", 6))

        try:
            patient = Patient.objects.get(pk=pid, owner=self.user)
        except Patient.DoesNotExist:
            raise ValueError("Patient not found or access denied.")

        # Build a simple textual summary (no LLM yet)
        problems = list(Condition.objects.filter(patient=patient, status="active").values_list("description", flat=True))
        meds = list(MedicationStatement.objects.filter(patient=patient, status="active").values_list("medication__name", flat=True))
        allergies = list(AllergyIntolerance.objects.filter(patient=patient, status="active").values_list("substance", flat=True))

        recent_obs = Observation.objects.filter(patient=patient).order_by("-datetime")[:10]
        obs_lines = [f"{o.datetime.date()} {o.name}: {o.value} {o.unit}".strip() for o in recent_obs]

        doc_count = DocumentReference.objects.filter(patient=patient).count()

        summary = {
            "patient": patient.full_name,
            "demographics": {"dob": str(patient.dob or ""), "sex": patient.sex},
            "active_problems": problems,
            "active_medications": meds,
            "allergies": allergies,
            "recent_observations": obs_lines,
            "documents_total": doc_count,
            "note": "This is a rule-based summary. Replace with LLM call for rich narrative."
        }
        return {"output": summary, "artifacts": []}
