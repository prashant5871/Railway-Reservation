# Generated by Django 5.0 on 2024-03-28 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('railway', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='email',
        ),
    ]
