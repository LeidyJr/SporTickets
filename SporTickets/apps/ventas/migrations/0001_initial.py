# Generated by Django 2.1.7 on 2019-02-27 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=100, verbose_name='Client')),
                ('seller', models.CharField(max_length=100, verbose_name='Seller')),
                ('date', models.DateTimeField(editable=False)),
                ('total', models.IntegerField()),
                ('finished', models.BooleanField()),
            ],
        ),
    ]
