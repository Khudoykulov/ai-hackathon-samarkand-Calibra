#!/usr/bin/env python
"""
Create migrations for all apps
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.management import execute_from_command_line


def create_migrations():
    """Create migrations for all apps"""

    apps = ['sensor', 'plant', 'ai_engine', 'controller']

    print("Creating migrations for all apps...")

    for app in apps:
        print(f"Creating migrations for {app}...")
        try:
            execute_from_command_line(['manage.py', 'makemigrations', app])
            print(f"✓ Migrations created for {app}")
        except Exception as e:
            print(f"✗ Error creating migrations for {app}: {str(e)}")

    print("\nApplying all migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ All migrations applied successfully")
    except Exception as e:
        print(f"✗ Error applying migrations: {str(e)}")


if __name__ == '__main__':
    create_migrations()
