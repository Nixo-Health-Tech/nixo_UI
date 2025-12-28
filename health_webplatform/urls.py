from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Pages
    path("", include(("home_app.urls", "home"), namespace="home")),
    path("about/", include(("about_app.urls", "about"), namespace="about")),
    path("contact/", include(("contact_app.urls", "contact"), namespace="contact")),

    # Core features
    path("emr/", include(("emr_app.urls", "emr"), namespace="emr")),
    path("models/", include(("ai_models_app.urls", "ai_models"), namespace="ai_models")),
    path("chat/", include(("chatbot_app.urls", "chatbot"), namespace="chatbot")),
    path("screening/breast/", include(("screening_app.breast.urls", "breast"), namespace="breast")),
    path("purchase/", include(("purchase_app.urls", "purchase"), namespace="purchase")),
    path("login/", include(("login_app.urls", "login"), namespace="login")),

    # Tools hub
    path("tools/", include(("platform_core.urls", "tools"), namespace="tools")),
]

# Serve media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
