# Generated by Django 4.2.1 on 2024-07-03 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='obj_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='patient',
            name='from_date',
            field=models.DateField(blank=True, null=True, verbose_name='Хона бант килинган сана'),
        ),
    ]