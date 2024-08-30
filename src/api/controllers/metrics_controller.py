# src/api/controllers/metrics_controller.py
import json

class MetricsController:
    @staticmethod
    def get_metrics():
        metrics = json.dumps({
            "classification_report": {
                "0": {
                    "precision": 0.9795918367346939,
                    "recall": 0.7272727272727273,
                    "f1-score": 0.8347826086956521,
                    "support": 66.0
                },
                "1": {
                    "precision": 0.7831325301204819,
                    "recall": 0.9848484848484849,
                    "f1-score": 0.87248322147651,
                    "support": 66.0
                },
                "accuracy": 0.8560606060606061,
                "macro avg": {
                    "precision": 0.8813621834275879,
                    "recall": 0.8560606060606061,
                    "f1-score": 0.8536329150860811,
                    "support": 132.0
                },
                "weighted avg": {
                    "precision": 0.8813621834275879,
                    "recall": 0.8560606060606061,
                    "f1-score": 0.8536329150860811,
                    "support": 132.0
                }
            },
            "confusion_matrix": [
                [
                    48,
                    18
                ],
                [
                    1,
                    65
                ]
            ],
            "class_areas": {
                "1": 0.25226229950540147,
                "0": 0.1489259358525864
            }
        })
        return metrics
