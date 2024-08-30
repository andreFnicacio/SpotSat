import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import os

@pytest.mark.django_db
def test_classification_api():
    client = APIClient()
    
    
    test_file_path = os.path.join(os.path.dirname(__file__), 'FAA_UTM18N_NAD83.tif')
    
    with open(test_file_path, 'rb') as test_file:
        response = client.post(
            reverse('classification'),  
            {'file': test_file},
            format='multipart'
        )
    
    assert response.status_code == status.HTTP_200_OK
    
    
    expected_keys = [
        'id', 'file_path', 'cloud_coverage', 'processing_date', 'geom', 'classification_result'
    ]
    for key in expected_keys:
        assert key in response.data
    
    
    assert response.data['classification_result']['classification'] in ['floresta', 'não-floresta']
    assert response.data['classification_result']['file_name'] == 'FAA_UTM18N_NAD83.tif'
