from django.contrib.gis.db import models

class Image(models.Model):
    file_path = models.CharField(max_length=255)  # Caminho do arquivo TIFF
    cloud_coverage = models.FloatField(null=True, blank=True)  # Cobertura de nuvens (se disponível)
    processing_date = models.DateField(auto_now_add=True)  # Data de processamento
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # Geometria da imagem
    classification_result = models.JSONField()  # Resultados da classificação e outras informações

    def __str__(self):
        return f"Image {self.id} - {self.file_path}"
