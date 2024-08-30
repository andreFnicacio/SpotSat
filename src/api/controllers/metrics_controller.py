# src/api/controllers/metrics_controller.py
import json

class MetricsController:
    @staticmethod
    def get_metrics():
        with open('/results/metrics/metrics_training_model.json', 'r') as file:
            metrics = json.load(file)
        return metrics
