from django.db import models

class Prediction(models.Model):
    prix_m2 = models.FloatField()
    population = models.IntegerField()
    property_tax = models.FloatField()
    last_year_property_tax = models.FloatField()

    # résultat simulé pour l'instant
    result = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.id} - {self.result}"
