from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import ToolSpec, Execution


def tool_list(request):
    tools = ToolSpec.objects.filter(is_active=True).order_by("name")
    return render(request, "platform_core/tool_list.html", {"tools": tools})


def tool_detail(request, slug):
    tool = get_object_or_404(ToolSpec, slug=slug, is_active=True)
    return render(request, "platform_core/tool_detail.html", {"tool": tool})


@require_http_methods(["GET", "POST"])
def run_tool(request, slug):
    tool = get_object_or_404(ToolSpec, slug=slug, is_active=True)

    if request.method == "GET":
        return render(request, "platform_core/run_form.html", {"tool": tool})

    # POST: payload را از textarea یا POST dict می‌گیریم
    import json
    raw = request.POST.get("payload")
    if raw:
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {"raw": raw}
    else:
        payload = request.POST.dict()

    wallet_service = None
    try:
        from purchase_app.services import WalletService
        wallet_service = WalletService(request.user)
    except Exception:
        pass

    from .services import execute_tool
    exec_obj = execute_tool(request.user, slug, payload, wallet_service=wallet_service)
    return redirect("tools:execution_detail", pk=exec_obj.pk)


def execution_detail(request, pk):
    exec_obj = get_object_or_404(Execution, pk=pk, user=request.user)
    return render(request, "platform_core/execution_detail.html", {"exec": exec_obj})
