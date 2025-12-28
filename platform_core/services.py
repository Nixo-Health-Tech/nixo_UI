import importlib
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import ToolSpec, Execution, ExecutionStatus

def _estimate_cost(adapter, tool, payload):
    if hasattr(adapter, "estimate_credits"):
        try:
            return int(adapter.estimate_credits(payload))
        except Exception:
            pass
    return int(getattr(tool, "credit_cost", 0) or 0)

def execute_tool(user, slug, payload: dict, wallet_service=None) -> Execution:
    tool = get_object_or_404(ToolSpec, slug=slug, is_active=True)

    module_path, cls_name = tool.adapter_path.rsplit(".", 1)
    Adapter = getattr(importlib.import_module(module_path), cls_name)
    adapter = Adapter(tool=tool, user=user, wallet_service=wallet_service)

    exec_obj = Execution.objects.create(
        user=user, tool=tool, input_payload=payload, status=ExecutionStatus.PENDING
    )

    cost = _estimate_cost(adapter, tool, payload)
    if wallet_service and cost > 0:
        wallet_service.ensure_balance(cost)

    exec_obj.status = ExecutionStatus.RUNNING
    exec_obj.started_at = timezone.now()
    exec_obj.save(update_fields=["status", "started_at"])

    try:
        result = adapter.run(payload)  # باید dict برگرداند
        output = result.get("output", result) if isinstance(result, dict) else {"output": str(result)}
        exec_obj.output_payload = output
        exec_obj.status = ExecutionStatus.SUCCEEDED

        if wallet_service and cost > 0:
            # WalletService.charge(amount, meta=...)
            wallet_service.charge(cost, meta={"tool": tool.slug, "execution_id": exec_obj.id})
    except Exception as e:
        exec_obj.status = ExecutionStatus.FAILED
        exec_obj.error_message = str(e)
    finally:
        exec_obj.finished_at = timezone.now()
        exec_obj.save()

    return exec_obj
