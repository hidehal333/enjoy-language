# Generated by Django 3.1.1 on 2020-11-11 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='diary',
            index=models.Index(fields=['id'], name='id_index'),
        ),
    ]