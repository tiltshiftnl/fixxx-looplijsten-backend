# TODO: Add tests
import logging
import os
from datetime import datetime
from multiprocessing import Process

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from api.fraudprediction.fraud_predict import FraudPredict
from api.fraudprediction.permissions import FraudPredictionApiKeyAuth
from utils.safety_lock import safety_lock

LOGGER = logging.getLogger(__name__)


@method_decorator(safety_lock, 'create')
class FraudPredictionScoringViewSet(ViewSet):
    """
    A view for triggering fraud scoring
    """
    permission_classes = [FraudPredictionApiKeyAuth | IsAuthenticated]

    def background_process(self):
        LOGGER.info('Started scoring background process')

        if hasattr(os, 'getppid'):
            LOGGER.info('Scoring process: {}'.format(os.getpid()))

        fraud_predict = FraudPredict()
        fraud_predict.start()

    def create(self, request):
        if hasattr(os, 'getppid'):
            LOGGER.info('Process kicking off scoring: {}'.format(os.getpid()))

        def detach_process():
            p = Process(target=self.background_process)
            p.start()

        p = Process(target=detach_process)
        p.start()

        json = {
            'message': 'Scoring Started {}'.format(str(datetime.now())),
        }
        return JsonResponse(json)
