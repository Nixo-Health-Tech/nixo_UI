from django import forms
class CheckoutForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label="تعداد")
