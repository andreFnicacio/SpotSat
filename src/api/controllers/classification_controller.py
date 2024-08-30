import joblib
import rasterio
from ..models.image_model import Image
from ..serializers.image_serializer import ImageSerializer
import uuid
import numpy as np

class ClassificationController:
    @staticmethod
    def classify_image(file):
        # Carregando o modelo treinado
        model = joblib.load('model/agent/random_forest_model.joblib')
        
        # Abrindo o arquivo TIFF e lendo os dados
        with rasterio.open(file) as src:
            data = src.read()  # Lê todas as bandas do raster
            data_reshaped = data.reshape((data.shape[0], -1)).T  # Prepara os dados para o modelo
            
            # Fazendo a previsão usando o modelo
            prediction = model.predict(data_reshaped)
            
            # Verificando se a imagem foi classificada como floresta ou não
            unique, counts = np.unique(prediction, return_counts=True)
            class_counts = dict(zip(unique, counts))
            classification = "floresta" if class_counts.get(1, 0) > class_counts.get(0, 0) else "não-floresta"

            # Captura de 'cloud_coverage', se disponível
            cloud_coverage = src.tags().get('CLOUD_COVER', 'N/A')
        
        # Preparando os metadados da imagem e a classificação para salvar no banco de dados
        image_metadata = {
            "idRaster": str(uuid.uuid4()),
            "classification": classification,
            "file_name": file.name,
            "width": src.width,
            "height": src.height,
            "crs": src.crs.to_string(),
            "transform": src.transform.to_gdal(),
            "count": src.count,
            "driver": src.driver,
            "cloud_coverage": cloud_coverage
        }
        
        # Salvando as informações no banco de dados
        image = Image.objects.create(
            file_path=file.name,
            metadata=image_metadata
        )
        
        return ImageSerializer(image).data
