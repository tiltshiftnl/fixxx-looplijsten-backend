# TODO: Add tests
import os
import threading
from multiprocessing import Process
import logging
from django.conf import settings
from django.http import FileResponse
from datetime import datetime
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from api.fraudprediction.permissions import FraudPredicionApiKeyAuth
from utils.safety_lock import safety_lock
from api.fraudprediction.fraud_predict import FraudPredict

LOGGER = logging.getLogger(__name__)

class FraudPredictionScoringViewSet(ViewSet):
    """
    A view for triggering fraud scoring
    """
    permission_classes = [FraudPredicionApiKeyAuth | IsAuthenticated]

    def background_process(self):

        def process():
            LOGGER.info('Started scoring background process')

            if hasattr(os, 'getppid'):
                LOGGER.info('Scoring process: {}'.format(os.getpid()))

            fraud_predict = FraudPredict()
            fraud_predict.start()

        p = Process(target=process)
        p.start()
        p.join()

    @safety_lock
    def create(self, request):
        t = threading.Thread(target=self.background_process)
        t.setDaemon(True)
        t.start()

        json = {
            'message': 'Scoring Started {}'.format(str(datetime.now())),
        }
        return JsonResponse(json)


class DebugViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @safety_lock
    def list(self, request):
        open_file = open(settings.DEBUG_LOG_FILE, 'rb')
        response = FileResponse(open_file, content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="%s"' % settings.DEBUG_LOG_FILE
        return response
