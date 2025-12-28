from django.apps import AppConfig

class EmrAppConfig(AppConfig):
    name = "emr_app"
    verbose_name = "EMR"

    def ready(self):
        # Place for signals if needed later
        pass
