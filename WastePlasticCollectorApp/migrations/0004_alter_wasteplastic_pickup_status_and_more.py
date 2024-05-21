# Generated by Django 5.0.3 on 2024-05-17 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WastePlasticCollectorApp', '0003_alter_requestpickup_agent_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteplastic',
            name='pickUp_status',
            field=models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('canceled', 'Canceled'), ('completed', 'Completed')], default='pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='wasteplasticrequestor',
            name='pickUp_status',
            field=models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('canceled', 'Canceled'), ('completed', 'Completed')], default='pending', max_length=100),
        ),
    ]
