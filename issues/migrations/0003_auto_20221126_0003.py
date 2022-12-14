# Generated by Django 4.1.3 on 2022-11-26 08:03

from django.db import migrations

def populate_status(apps, schemaditor):
    statuses = {
        'To Do': 'This issue is not yet started',
        'In Progress': 'This issue is currently being worked on',
        'Done': 'This issue is completed'

    }
    Status = apps.get_model('issues', 'Status')
    for key, value in statuses.items():
        Status_obj = Status(name=key, description=value)
        Status_obj.save()

def populate_priority(apps, schemaditor):
    priorities = {
        'Low': 'This issue is not urgent',
        'Medium': 'This issue is of medium priority',
        'High': 'This issue is urgent'

    }
    Priority = apps.get_model('issues', 'Priority')
    for key, value in priorities.items():
        pr_obj = Priority(name=key, description=value)
        pr_obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0002_issue_delete_issues'),
    ]

    operations = [
        migrations.RunPython(populate_status),
        migrations.RunPython(populate_priority),
    ]
