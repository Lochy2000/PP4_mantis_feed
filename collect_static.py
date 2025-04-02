import os
import sys
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mantisfeed.settings')

# Set development flag to ensure Django uses correct settings
os.environ['DEVELOPMENT'] = 'True'

# Initialize Django
django.setup()

# Import Django's management module
from django.core.management import call_command

# Run collectstatic command
call_command('collectstatic', '--noinput', '--clear')

print("Static files collected successfully!")
