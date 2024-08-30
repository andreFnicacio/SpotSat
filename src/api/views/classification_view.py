from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..controllers.classification_controller import ClassificationController

class ClassificationView(APIView):
    def post(self, request):
        # Verifica se o arquivo está presente na requisição
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        
        try:
            result = ClassificationController.classify_image(file)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
