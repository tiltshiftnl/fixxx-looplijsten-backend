# TODO: Add tests
import threading
from django.core import management
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from api.fraudprediction.permissions import FraudPredicionApiKeyAuth
from utils.safety_lock import safety_lock
from api.fraudprediction.management.commands import fraud_predict

class FraudPredictionScoringViewSet(ViewSet):
    """
    A view for triggering fraud scoring
    """
    permission_classes = [FraudPredicionApiKeyAuth | IsAuthenticated]

    def background_process(self):
        management.call_command(fraud_predict.Command())

    @safety_lock
    def create(self, request):
        # Note: At some point it might be better to use asynchronous task queue/job
        t = threading.Thread(target=self.background_process)
        t.setDaemon(True)
        t.start()
        return HttpResponse('Scoring Started')
