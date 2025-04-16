from django.db import migrations, models
import django.db.models.deletion

def create_all_groups_and_assign(apps, schema_editor):
    Group = apps.get_model('admin_dashboard', 'Group')
    Announcement = apps.get_model('admin_dashboard', 'Announcement')
    
    # Create "All Groups" if it doesn't exist
    all_groups, created = Group.objects.get_or_create(
        id=1,
        defaults={'name': 'All Groups'}
    )
    
    # Assign null announcements to "All Groups"
    Announcement.objects.filter(group__isnull=True).update(group=all_groups)

def reverse_migration(apps, schema_editor):
    Group = apps.get_model('admin_dashboard', 'Group')
    Announcement = apps.get_model('admin_dashboard', 'Announcement')
    
    # Set announcements back to null
    Announcement.objects.filter(group_id=1).update(group=None)
    
    # Delete the "All Groups" group
    Group.objects.filter(id=1).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0007_remove_timetable_pdf_file_timetable_pdf_data_and_more'),
    ]

    operations = [
        # First run the data migration
        migrations.RunPython(
            create_all_groups_and_assign,
            reverse_migration
        ),
        
        # Then alter the field to make it non-nullable
        migrations.AlterField(
            model_name='announcement',
            name='group',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='announcements',
                to='admin_dashboard.group'
            ),
        ),
    ]