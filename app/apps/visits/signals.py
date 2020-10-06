import logging

from apps.visits.models import Visit
from django.db.models import signals
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(signals.post_save, sender=Visit)
def capture_visit_meta_data(sender, instance, **kwargs):
    visit = instance
    fraud_prediction = instance.itinerary_item.case.fraud_prediction
    print(visit)
    print(fraud_prediction)
