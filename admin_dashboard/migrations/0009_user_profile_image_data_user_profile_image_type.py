# Generated by Django 5.2 on 2025-04-15 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0008_create_all_groups_and_handle_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image_data',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_image_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
