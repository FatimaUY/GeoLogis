from django.db import models

# Create your models here.
class MarketData(models.Model):
    city = models.CharField(max_length=100)
    property_type = models.CharField(max_length=50)
    average_price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.city} - {self.property_type} - {self.average_price}"