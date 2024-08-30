from ..models.image_model import Image
from ..serializers.image_serializer import ImageSerializer

class ConsultationController:
    @staticmethod
    def get_classifications(idRaster=None, date_range=None, cloud_coverage=None):
        # Inicializa o queryset baseando-se na existência dos filtros
        classifications = Image.objects.all()

        # Filtro por idRaster
        if idRaster:
            classifications = classifications.filter(idRaster=idRaster)
        
        # Filtro por intervalo de datas
        if date_range:
            start_date, end_date = date_range
            classifications = classifications.filter(processing_date__range=[start_date, end_date])
        
        # Filtro por cobertura de nuvens
        if cloud_coverage is not None:
            classifications = classifications.filter(cloud_coverage=cloud_coverage)
        
        return ClassificationSerializer(classifications, many=True).data
