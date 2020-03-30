# TODO: Add tests
import threading
import logging
from datetime import datetime
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
        LOGGER.info('Started scoring background process')
        print('Started scoring background process')
        management.call_command(fraud_predict.Command())

    @safety_lock
    def create(self, request):
        t = threading.Thread(target=self.background_process)
        t.setDaemon(True)
        t.start()

        json = {
            'message': 'Scoring Started {}'.format(str(datetime.now())),
        }
        return JsonResponse(json)
