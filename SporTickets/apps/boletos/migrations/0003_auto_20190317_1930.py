# Generated by Django 2.1.7 on 2019-03-18 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boletos', '0002_auto_20190317_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boletos_de_la_venta', to='ventas.Sale', verbose_name='Sale'),
        ),
    ]
