import logging

from apps.itinerary.models import ItineraryItem
from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver
from tenacity import RetryError
from utils.queries_zaken_api import push_itinerary_item

logger = logging.getLogger(__name__)

# TODO: Tests for this
# TODO: Should log if a push fails
@receiver(signals.post_save, sender=ItineraryItem)
def create_itinerary_item_signal(instance, created, **kwargs):
    if created and instance.case:
        try:
            logger.info(f"Signal for pushing itinerary item {instance}.")
            if settings.PUSH_ZAKEN:
                push_itinerary_item(instance)
        except RetryError as e:
            logger.error(f"Pushing case failed: {str(e)}")
