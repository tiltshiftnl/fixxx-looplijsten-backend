# TODO: Add tests
import threading
import logging
import glob
import os
from datetime import datetime
from django.conf import settings
from django.core import management
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from api.fraudprediction.permissions import FraudPredicionApiKeyAuth
from utils.safety_lock import safety_lock
from api.fraudprediction.management.commands import fraud_predict

LOGGER = logging.getLogger(__name__)

class FraudPredictionScoringViewSet(ViewSet):
    """
    A view for triggering fraud scoring
    """
    permission_classes = [FraudPredicionApiKeyAuth | IsAuthenticated]

    def background_process(self):
        LOGGER.error('Started background process')
        management.call_command(fraud_predict.Command())

    @safety_lock
    def create(self, request):
        # Before starting any threads, get the contents of the cache directory
        dir = settings.FRAUD_PREDICTION_CACHE_DIR
        files = glob.glob(os.path.join(dir, '*'))

        # Note: At some point it might be better to use asynchronous task queue/job
        t = threading.Thread(target=self.background_process)
        t.setDaemon(True)
        t.start()

        json = {
            'message': 'Scoring Started {}'.format(str(datetime.now())),
            'cache': files
        }
        return JsonResponse(json)
