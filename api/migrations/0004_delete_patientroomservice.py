# Generated by Django 4.2.1 on 2023-05-31 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_roominfo_patient_alter_patient_doctor_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PatientRoomService',
        ),
    ]
