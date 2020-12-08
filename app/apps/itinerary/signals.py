import logging

from apps.itinerary.models import ItineraryItem
from apps.itinerary.tasks import push_itinerary_item
from django.conf import settings
from django.db import transaction
from django.db.models import signals
from django.dispatch import receiver
from tenacity import RetryError

logger = logging.getLogger(__name__)

# TODO: Tests for this
# TODO: Should log if a push fails
@receiver(signals.post_save, sender=ItineraryItem)
def create_itinerary_item_signal(instance, created, **kwargs):
    if created and instance.case:
        try:
            logger.info(f"Signal for pushing itinerary item {instance}.")
            transaction.on_commit(push_itinerary_item.s(instance.pk).delay)
        except RetryError as e:
            logger.error(f"Pushing case failed: {str(e)}")
