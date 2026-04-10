from django.db import models
from django.conf import settings

class Prediction(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="predictions"
    )


    prix_m2 = models.FloatField()
    population = models.IntegerField()
    property_tax = models.FloatField()
    last_year_property_tax = models.FloatField()

    # résultat simulé pour l'instant
    result = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_name = self.user.username if self.user else "Anonyme"
        return f"Prediction {self.id} - {user_name} ({self.result})"
