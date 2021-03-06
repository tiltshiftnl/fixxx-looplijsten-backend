from django.apps import AppConfig
from health_check.plugins import plugin_dir


class HealthConfig(AppConfig):
    name = "apps.health"

    def ready(self):
        from .health_checks import BAGServiceCheck, BWVDatabaseCheck, ZakenServiceCheck

        plugin_dir.register(BAGServiceCheck)
        plugin_dir.register(BWVDatabaseCheck)
        plugin_dir.register(ZakenServiceCheck)
