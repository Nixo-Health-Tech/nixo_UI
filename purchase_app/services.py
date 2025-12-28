from __future__ import annotations
from datetime import timedelta
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import Wallet, UsageLog, Order, OrderStatus, Subscription, SubscriptionStatus, Price, PriceKind

class InsufficientCredits(Exception):
    pass

class WalletService:
    def __init__(self, user):
        self.user = user

    def get_wallet(self) -> Wallet:
        wallet, _ = Wallet.objects.get_or_create(user=self.user)
        return wallet

    def ensure_balance(self, needed: int):
        w = self.get_wallet()
        if w.credits < int(needed):
            raise InsufficientCredits("اعتبار کافی نیست.")

    def charge(self, amount: int, meta: dict=None):
        w = self.get_wallet()
        w.credits -= int(amount)
        w.save(update_fields=["credits"])
        UsageLog.objects.create(user=self.user, credits_spent=int(amount), meta=meta or {})

    def add_credits(self, amount: int, meta: dict=None):
        w = self.get_wallet()
        w.credits += int(amount)
        w.save(update_fields=["credits"])
        UsageLog.objects.create(user=self.user, credits_spent=-int(amount), meta=meta or {"type": "topup"})

class CheckoutService:
    """Manual checkout flow; replace 'mark_paid' with Stripe/PayPal later."""

    @staticmethod
    @transaction.atomic
    def create_order(user, price: Price, quantity: int=1) -> Order:
        total = price.unit_amount * Decimal(quantity)
        order = Order.objects.create(
            user=user, price=price, quantity=quantity,
            total_amount=total, currency=price.currency
        )
        return order

    @staticmethod
    @transaction.atomic
    def mark_paid(order: Order):
        order.status = OrderStatus.PAID
        order.paid_at = timezone.now()
        order.save(update_fields=["status", "paid_at"])
        price = order.price
        if price.kind == PriceKind.ONE_TIME and price.credits_included > 0:
            WalletService(order.user).add_credits(price.credits_included * order.quantity, meta={"order_id": order.id})
        elif price.kind == PriceKind.RECURRING:
            now = timezone.now()
            Subscription.objects.create(
                user=order.user, price=price, status=SubscriptionStatus.ACTIVE,
                current_period_start=now, current_period_end=now + timedelta(days=30),
            )
