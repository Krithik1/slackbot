from django.db import models

class KitchenItem(models.Model):
    name = models.CharField(max_length=100)
    expiration_date = models.DateField(blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)