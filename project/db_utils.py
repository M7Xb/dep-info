import mysql.connector
from django.conf import settings

def create_database_if_not_exists():
    try:
        # Connect to MySQL without specifying a database
        conn = mysql.connector.connect(
            host=settings.DATABASES['default']['HOST'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            port=settings.DATABASES['default']['PORT'],
        )
        cursor = conn.cursor()

        # Create database if it doesn't exist
        db_name = settings.DATABASES['default']['NAME']
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        print(f"Database '{db_name}' created or already exists.")
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error creating database: {e}")
        raise