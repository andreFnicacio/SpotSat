# src/api/views/consultation_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from ..controllers.consultation_controller import ConsultationController

class ConsultationView(APIView):
    def get(self, request):
        idRaster = request.query_params.get('idRaster')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        cloud_coverage = request.query_params.get('cloud_coverage')
        date_range = (start_date, end_date) if start_date and end_date else None
        result = ConsultationController.get_classifications(idRaster=idRaster, date_range=date_range, cloud_coverage=cloud_coverage)
        return Response(result, status=200)
