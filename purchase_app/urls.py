from django.urls import path
from . import views
app_name = "purchase"
urlpatterns = [
    path("", views.plans, name="plans"),
    path("checkout/<int:price_id>/", views.checkout, name="checkout"),
    path("success/<int:order_id>/", views.success, name="success"),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path("subscriptions/<int:sub_id>/cancel/", views.cancel_subscription, name="cancel_subscription"),
]
