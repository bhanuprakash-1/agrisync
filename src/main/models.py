from django.db import models
from src.oauth.models import Farmer


class FarmerDetails(models.Model):
    """
    Choices For Soil type and Crop type for farmers
    """
    soil_type = (
        (1, 'Alluvial'),
        (2, 'Black(Regur)'),
        (3, 'Red & Yellow'),
        (4, 'Laterite'),
        (5, 'Arid'),
        (6, 'Saline'),
        (7, 'Peaty and Marshy'),
        (8, 'Forest & Mountain'),
    )
    primary_crop = (
        (1, 'Rice'),
        (2, 'Wheat'),
        (3, 'Pulses'),
    )

    """
    Various Model Fields
    """
    farmer = models.ForeignKey(Farmer, on_delete= models.CASCADE)
    soil = models.CharField(choices=soil_type, blank=False)
    primary_crop = models.CharField(choices=primary_crop, blank=False)
    secondary_crop = models.CharField(blank=True)

    def __str__(self):
        return self.farmer.first_name