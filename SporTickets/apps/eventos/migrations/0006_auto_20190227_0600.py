# Generated by Django 2.1.7 on 2019-02-27 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0005_auto_20190226_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos_del_tipo', to='eventos.EventType'),
        ),
        migrations.AlterField(
            model_name='eventlocation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evento_localidades_del_evento', to='eventos.Event'),
        ),
        migrations.AlterField(
            model_name='eventlocation',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evento_localidades_de_localidades', to='eventos.Location'),
        ),
    ]
