# Generated by Django 5.0.3 on 2024-09-01 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusers',
            name='is_orginization',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customusers',
            name='latitude',
            field=models.FloatField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customusers',
            name='longitude',
            field=models.FloatField(blank=True, max_length=50, null=True),
        ),
    ]
