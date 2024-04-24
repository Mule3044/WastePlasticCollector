# Generated by Django 5.0.3 on 2024-04-22 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WastePlasticCollectorApp', '0004_remove_wasteplastic_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wasteplasticrequestor',
            name='status',
        ),
        migrations.AddField(
            model_name='wasteplasticrequestor',
            name='recent_activity',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=100),
        ),
        migrations.AddField(
            model_name='wasteplasticrequestor',
            name='request_history',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=100),
        ),
    ]
