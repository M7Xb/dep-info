# Generated by Django 5.2 on 2025-04-12 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', 'xxxx_update_user_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
    ]
