# Generated by Django 4.2.13 on 2024-06-29 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_projects_members_alter_projects_title_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projects',
            old_name='user',
            new_name='created_by',
        ),
    ]
