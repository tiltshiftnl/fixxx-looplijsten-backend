from django.apps import AppConfig


class ItineraryConfig(AppConfig):
    name = "apps.itinerary"

    def ready(self):
        import apps.itinerary.signals
