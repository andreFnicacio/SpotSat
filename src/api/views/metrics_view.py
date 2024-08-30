# src/api/views/metrics_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from ..controllers.metrics_controller import MetricsController

class MetricsView(APIView):
    def get(self, request):
        metrics = MetricsController.get_metrics()
        return Response(metrics, status=200)
