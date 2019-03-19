from django.db import models
from django.utils import timezone


class Sale(models.Model):
    client = models.CharField(max_length=100, verbose_name="Client")
    seller = models.CharField(max_length=100, verbose_name="Seller")
    date = models.DateTimeField(editable=False)
    subtotal = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return ("%s %s (%s)"%(self.client, self.seller, self.date))

    def save(self, *args, **kwargs):
        
        if not self.id:
            self.date = timezone.now()
        return super(Sale, self).save(*args, **kwargs)

    @staticmethod
    def obtener_sale_active(request, client, seller):
        if "venta_activa" in request.session:
            return Sale.objects.get(id=request.session["venta_activa"])
        else:
            sale = Sale.objects.create(client=client, seller=seller)
            request.session["venta_activa"] = sale.id
            return sale