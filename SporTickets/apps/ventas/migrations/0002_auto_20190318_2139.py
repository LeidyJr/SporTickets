# Generated by Django 2.1.7 on 2019-03-19 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='subtotal',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sale',
            name='finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]