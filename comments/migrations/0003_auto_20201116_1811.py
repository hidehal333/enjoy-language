# Generated by Django 3.1.1 on 2020-11-16 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20201116_1755'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'Comments'},
        ),
    ]