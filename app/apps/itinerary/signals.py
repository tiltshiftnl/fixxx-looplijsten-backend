import logging

from apps.itinerary.models import ItineraryItem
from django.db.models import signals
from django.dispatch import receiver
from tenacity import RetryError
from utils.queries_zaken_api import push_case, push_checked_action

logger = logging.getLogger(__name__)


# TODO: Tests for this
# TODO: Should log if a push fails
@receiver(signals.post_save, sender=ItineraryItem)
def create_itinerary_item_signal(instance, created, **kwargs):
    if created and instance.case:
        try:
            case_id = instance.case.case_id
            logger.info(f"Signal for pushing case {case_id}")
            push_case(case_id)
        except RetryError as e:
            logger.error(f"Pushing case failed: {str(e)}")


# TODO: With the new visit module this is deprecated. Update to push visit data.
@receiver(signals.pre_save, sender=ItineraryItem)
def checked_itinerary_item_signal(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
        if obj and not obj.checked == instance.checked:  # Field has changed
            push_checked_action(instance.case.case_id, instance.checked)
    except (sender.DoesNotExist, RetryError) as e:
        logger.error(f"Pushing case visit failed: {str(e)}")
