import joblib
import rasterio
from rasterio.io import MemoryFile
from ..models.image_model import Image
from ..serializers.image_serializer import ImageSerializer
import uuid
import numpy as np

class ClassificationController:
    @staticmethod
    def classify_image(file):
        # Load the trained model
        model = joblib.load('model/agent/random_forest_model.joblib')

        # Open the file using rasterio's MemoryFile
        with MemoryFile(file) as memfile:
            with memfile.open() as src:
                data = src.read()  # Read all bands from the raster
                data_reshaped = data.reshape((data.shape[0], -1)).T  # Prepare data for model

                # Perform the prediction
                prediction = model.predict(data_reshaped)
                unique, counts = np.unique(prediction, return_counts=True)
                class_counts = dict(zip(unique, counts))
                classification = "floresta" if class_counts.get(1, 0) > class_counts.get(0, 0) else "não-floresta"

                # Capture 'cloud_coverage', if available
                cloud_coverage = src.tags().get('CLOUD_COVER', 'N/A')
                idRaster = str(uuid.uuid4())
                # Prepare metadata to save in the database
                image_metadata = {
                    "idRaster": idRaster,
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

                # Save to database
                image = Image.objects.create(
                    file_path=file.name,
                    classification_result=image_metadata
                )

        return ImageSerializer(image).data
