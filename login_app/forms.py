from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["full_name", "phone_number", "email"]  # ایمیل اختیاری است

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"].replace(" ", "").replace("-", "")
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("این شماره تلفن قبلاً ثبت شده است.")
        return phone

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            self.add_error("password2", "رمز عبور و تکرار آن یکسان نیست.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PhoneAuthenticationForm(AuthenticationForm):
    # AuthenticationForm expects a field named 'username' that maps to USERNAME_FIELD.
    username = forms.CharField(label="شماره تلفن")
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
