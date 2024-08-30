import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
def test_consultation_api():
    client = APIClient()
    
    
    response = client.get(reverse('consultation'), {'idRaster': 'some-valid-uuid'})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert 'classification_result' in response.data[0]
    assert response.data[0]['classification_result']['idRaster'] == 'some-valid-uuid'

    
    response = client.get(reverse('consultation'), {'start_date': '2023-01-01', 'end_date': '2023-12-31'})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0  

    
    response = client.get(reverse('consultation'), {'idRaster': 'invalid-uuid'})
    assert response.status_code == status.HTTP_404_NOT_FOUND  

    
    response = client.get(reverse('consultation'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0  
