import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
def test_metrics_api():
    client = APIClient()
    
    response = client.get(reverse('metrics'))
    
    assert response.status_code == status.HTTP_200_OK
    
    expected_keys = ['classification_report', 'confusion_matrix', 'class_areas']
    for key in expected_keys:
        assert key in response.data
    
    assert isinstance(response.data['classification_report'], dict)
    assert isinstance(response.data['confusion_matrix'], list)
    assert isinstance(response.data['class_areas'], dict)
