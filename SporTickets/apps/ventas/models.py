from django.db import models
from django.utils import timezone
from apps.usuarios.models import User


class Venta(models.Model):

    cliente = models.ForeignKey(User, related_name="compras_del_usuario", on_delete=models.CASCADE, null=True)
    vendedor = models.ForeignKey(User, related_name="ventas_del_vendedor", on_delete=models.CASCADE, null=True)
    fecha = models.DateTimeField(editable=False)
    subtotal = models.IntegerField(default=0)
    iva = models.FloatField(default=0)
    total = models.IntegerField(default=0)
    terminada = models.BooleanField(default=False)

    def __str__(self):
        return ("%s %s (%s)"%(self.vendedor, self.fecha, self.total))

    def save(self, *args, **kwargs):
        
        if not self.id:
            self.fecha = timezone.now()
        return super(Venta, self).save(*args, **kwargs)

    def eliminar_boleto(self, boleto):
        localidad_del_evento = boleto.localidades_evento
        localidad_del_evento.disponibilidad += 1
        localidad_del_evento.save()
        boleto.delete()

    @staticmethod
    def obtener_venta_activa(request, cliente, vendedor):
        if "venta_activa" in request.session:
            return Venta.objects.get(id=request.session["venta_activa"])
        else:
            venta = Venta.objects.create(cliente=cliente, vendedor=vendedor)
            request.session["venta_activa"] = venta.id
            return venta

    @staticmethod
    def obtener_venta(request):
        if "venta_activa" in request.session:
            return Venta.objects.get(id=request.session["venta_activa"])
        return None