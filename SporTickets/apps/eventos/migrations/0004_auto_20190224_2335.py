# Generated by Django 2.1.7 on 2019-02-25 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0003_auto_20190216_0032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='eventlocation',
            options={'ordering': ['event', 'location']},
        ),
        migrations.AddField(
            model_name='eventlocation',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tipos_de_evento', to='eventos.EventType'),
        ),
        migrations.AlterField(
            model_name='eventlocation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='localidades_del_evento', to='eventos.Event'),
        ),
        migrations.AlterField(
            model_name='eventlocation',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='localidades', to='eventos.Location'),
        ),
        migrations.AlterField(
            model_name='location',
            name='event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='localidades_del_tipo', to='eventos.EventType', verbose_name='Event type'),
        ),
    ]
