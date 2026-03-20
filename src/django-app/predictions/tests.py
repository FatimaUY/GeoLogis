from django.test import TestCase
from rest_framework.test import APIClient

class PredictionTest(TestCase):
    def test_predict(self):
        client = APIClient()

        response = client.post("/api/predictions/predict/", {
            "prix_m2": 3000,
            "property_tax": 1000,
            "last_year_property_tax": 900,
            "population": 50000
        }, format="json")

        self.assertEqual(response.status_code, 200)