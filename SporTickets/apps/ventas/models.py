from django.db import models
from django.utils import timezone


class Sale(models.Model):
    client = models.CharField(max_length=100, verbose_name="Client")
    seller = models.CharField(max_length=100, verbose_name="Seller")
    date = models.DateTimeField(editable=False)
    total = models.IntegerField()
    finished = models.BooleanField()

    def __str__(self):
        return ("%s %s (%s)"%(self.client, self.seller, self.date))

    def save(self, *args, **kwargs):
        
        if not self.id:
            self.date = timezone.now()
        return super(Sale, self).save(*args, **kwargs)
