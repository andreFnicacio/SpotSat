# src/api/urls.py
from django.urls import path
from .views.classification_view import ClassificationView
from .views.consultation_view import ConsultationView
from .views.metrics_view import MetricsView

urlpatterns = [
    path('classification/', ClassificationView.as_view(), name='classification'),
    path('consultation/', ConsultationView.as_view(), name='consultation'),
    path('metrics/', MetricsView.as_view(), name='metrics'),
]
