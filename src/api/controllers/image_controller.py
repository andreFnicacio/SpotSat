from ..models.image_model import Image
from ..serializers.image_serializer import ImageSerializer

class ImageController:
    @staticmethod
    def create_image(data):
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return serializer.errors

    @staticmethod
    def get_images(filters=None):
        images = Image.objects.filter(**filters) if filters else Image.objects.all()
        return ImageSerializer(images, many=True).data
