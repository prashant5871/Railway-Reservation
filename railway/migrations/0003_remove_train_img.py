# Generated by Django 5.0 on 2024-03-28 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('railway', '0002_remove_register_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='train',
            name='img',
        ),
    ]
