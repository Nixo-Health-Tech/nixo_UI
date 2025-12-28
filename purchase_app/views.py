from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Price, Order, Subscription, SubscriptionStatus
from .forms import CheckoutForm
from .services import CheckoutService


def plans(request):
    products = Product.objects.filter(active=True).prefetch_related("prices")
    return render(request, "purchase/plans.html", {"products": products})


def checkout(request, price_id):
    price = get_object_or_404(Price, pk=price_id, active=True)
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data["quantity"]
            order = CheckoutService.create_order(request.user, price, qty)
            CheckoutService.mark_paid(order)  # simulate payment success
            return redirect("purchase:success", order_id=order.id)
    else:
        form = CheckoutForm()
    return render(request, "purchase/checkout.html", {"price": price, "form": form})


def success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, "purchase/success.html", {"order": order})


def subscriptions(request):
    subs = Subscription.objects.filter(user=request.user).select_related("price","price__product")
    return render(request, "purchase/subscriptions.html", {"subs": subs})


def cancel_subscription(request, sub_id):
    sub = get_object_or_404(Subscription, pk=sub_id, user=request.user)
    if request.method == "POST":
        sub.status = SubscriptionStatus.CANCELED
        sub.cancel_at_period_end = True
        sub.save(update_fields=["status","cancel_at_period_end"])
        return redirect("purchase:subscriptions")
    return render(request, "purchase/cancel_confirm.html", {"sub": sub})
