from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import connection
import os

User = get_user_model()

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            count = cursor.fetchone()[0]
            
        if count == 0:
            User.objects.create_superuser(
                username=os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@department.com'),
                email=os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@department.com'),
                password=os.environ.get('DEFAULT_ADMIN_PASSWORD', 'Admin@123'),
                first_name='Admin',
                last_name='User',
                role='admin',
                is_active=True
            )
            print('Default admin user created successfully!')
    except Exception as e:
        print(f'Error creating default admin: {str(e)}')
