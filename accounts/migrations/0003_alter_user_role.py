# Generated by Django 5.2 on 2025-04-14 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_options_alter_user_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('teacher', 'Teacher'), ('admin', 'Admin')], default='user', max_length=10),
        ),
    ]
