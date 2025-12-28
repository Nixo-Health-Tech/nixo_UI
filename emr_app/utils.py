# emr_app/utils.py
from django.apps import apps

def get_model(app_label, model_name):
    return apps.get_model(app_label, model_name)

def field_names(model):
    return [f.name for f in model._meta.get_fields()]

def has_field(model, name):
    return name in field_names(model)

def get_or_create_self_patient(user):
    """
    تلاش می‌کند Patient متصل به کاربر را پیدا کند؛ اگر نبود، با حداقل اطلاعات می‌سازد.
    سناریوهای رایج:
      - Patient.owner -> FK به کاربر
      - Patient.user  -> OneToOne/ FK به کاربر
    """
    Patient = get_model("emr_app", "Patient")
    fn = field_names(Patient)

    qs = Patient.objects.all()
    # جستجو بر اساس فیلدهای متداول
    if "owner" in fn:
        obj = qs.filter(owner=user).first()
        if obj:
            return obj
    if "user" in fn:
        obj = qs.filter(user=user).first()
        if obj:
            return obj

    # اگر چیزی نبود، می‌سازیم (تا جای ممکن فیلدها را پر می‌کنیم)
    kwargs = {}
    if "owner" in fn:
        kwargs["owner"] = user
    if "user" in fn and "user" not in kwargs:
        kwargs["user"] = user
    if "full_name" in fn:
        kwargs["full_name"] = getattr(user, "full_name", "") or str(user)
    if "identifier" in fn:
        kwargs["identifier"] = f"U{user.pk:06d}"

    return Patient.objects.create(**kwargs)
