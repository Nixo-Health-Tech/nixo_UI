from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ----------------------------
# Custom User Manager
# ----------------------------
class CustomUserManager(BaseUserManager):
    """مدیر کاربر با ورود بر پایه‌ی شماره تلفن."""

    @staticmethod
    def _normalize_phone(phone: str) -> str:
        # ساده: فاصله/داش را حذف می‌کند. (برای E.164: +123456789...)
        if not phone:
            return phone
        return phone.replace(" ", "").replace("-", "")

    def create_user(
        self,
        phone_number: str,
        full_name: str,
        password: str | None = None,
        *,
        email: str | None = None,
        role: str = "patient",
        locale: str = "fa",
        timezone_name: str = "UTC",
        plan: str = "basic",
        remaining_questions: int = 0,
    ):
        if not phone_number:
            raise ValueError("شماره تلفن باید وارد شود")

        phone_number = self._normalize_phone(phone_number)

        user = self.model(
            phone_number=phone_number,
            full_name=full_name,
            email=self.normalize_email(email) if email else None,
            role=role,
            locale=locale,
            timezone=timezone_name,
            # نگه‌داشتن برای سازگاری عقب‌رو (deprecated)
            plan=plan,
            remaining_questions=remaining_questions,
            is_active=True,
            is_staff=False,
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        phone_number: str,
        full_name: str,
        password: str | None = None,
        **extra,
    ):
        # سوپریوزر باید is_staff و is_superuser داشته باشد
        user = self.create_user(
            phone_number=phone_number,
            full_name=full_name,
            password=password,
            role=extra.get("role", "admin"),
            plan=extra.get("plan", "advanced"),                 # فقط برای سازگاری قدیمی
            remaining_questions=extra.get("remaining_questions", 999),
            email=extra.get("email"),
            locale=extra.get("locale", "fa"),
            timezone_name=extra.get("timezone_name", "UTC"),
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# ----------------------------
# Custom User Model
# ----------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    کاربر اصلی پلتفرم:
    - ورود با phone_number (E.164)
    - نقش کاربری برای تمایز بیمار/کلینیسین/ادمین
    - فیلدهای کاربردی برای تجربه کاربری و انطباق
    - فیلدهای plan/remaining_questions فقط برای سازگاری قدیمی (به‌جای آن از purchase_app استفاده کنید)
    """

    # نقش‌ها
    ROLE_CHOICES = [
        ("patient", "Patient / کاربر عادی"),
        ("clinician", "Clinician / ارائه‌دهنده"),
        ("admin", "Organization Admin / ادمین"),
    ]

    # (قدیمی) طرح‌ها — توصیه می‌شود از subscriptionها در purchase_app استفاده کنید
    PLAN_CHOICES = [
        ("basic", "Basic (deprecated)"),
        ("advanced", "Advanced (deprecated)"),
    ]

    # هویت
    phone_regex = RegexValidator(
        regex=r"^\+?[1-9]\d{7,14}$",
        message="شماره تلفن باید در قالب E.164 باشد (مثال: +989121234567).",
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_regex],
        help_text="ورود با شماره تلفن (E.164)."
    )
    email = models.EmailField(
        unique=True, null=True, blank=True,
        help_text="اختیاری، برای اعلان‌ها و بازیابی."
    )
    full_name = models.CharField(max_length=100)

    # نقش و تنظیمات کاربر
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="patient")
    locale = models.CharField(max_length=10, default="fa", help_text="زبان/محلی‌سازی پیش‌فرض رابط.")
    timezone = models.CharField(max_length=50, default="UTC", help_text="منطقهٔ زمانی کاربر.")

    # وضعیت عضویت/انطباق
    date_joined = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    tos_accepted = models.BooleanField(default=False, help_text="پذیرش شرایط استفاده.")
    tos_accepted_at = models.DateTimeField(null=True, blank=True)
    marketing_opt_in = models.BooleanField(default=False)

    # وضعیت سیستم
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)   # برای دسترسی به /admin
    # is_superuser از PermissionsMixin می‌آید

    # فیلدهای قدیمی (برای سازگاری — پیشنهاد می‌شود در آینده حذف شوند)
    plan = models.CharField(
        max_length=10, choices=PLAN_CHOICES, default="basic",
        help_text="(Deprecated) لطفاً از subscriptions در purchase_app استفاده کنید."
    )
    remaining_questions = models.IntegerField(
        default=0,
        help_text="(Deprecated) به‌جای این از Wallet/UsageLog برای محدودیت استفاده بهره ببرید."
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]  # هنگام createsuperuser نیز ایمیل اختیاری است

    objects = CustomUserManager()

    class Meta:
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["phone_number"]),
            models.Index(fields=["email"]),
        ]
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.full_name or self.phone_number

    # کمک‌متدها
    def touch_last_seen(self):
        self.last_seen = timezone.now()
        self.save(update_fields=["last_seen"])

    @property
    def display_name(self) -> str:
        return self.full_name or self.phone_number

    # نمونه‌هایی برای یکپارچه‌سازی با purchase_app (اختیاری)
    @property
    def wallet_credits(self) -> int:
        try:
            return self.wallet.credits  # OneToOne از purchase_app.Wallet اگر ساخته شده باشد
        except Exception:
            return 0

    def has_active_subscription(self, product_slug: str | None = None) -> bool:
        """
        اگر purchase_app نصب باشد، بررسی می‌کند کاربر اشتراک فعال دارد یا خیر.
        اگر product_slug داده شود، مخصوص همان محصول چک می‌کند.
        """
        try:
            from purchase_app.models import Subscription, SubscriptionStatus
            qs = Subscription.objects.filter(user=self, status=SubscriptionStatus.ACTIVE)
            if product_slug:
                qs = qs.filter(price__product__slug=product_slug)
            return qs.exists()
        except Exception:
            return False
