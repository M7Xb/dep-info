from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_role'),  # Update this to your last migration
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_image',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_image_data',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_image_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]