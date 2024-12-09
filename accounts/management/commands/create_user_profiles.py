from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Creates user profile for exisitng users'
    
    def handle(self, **kwargs):
        users = User.objects.filter(userprofile__isnull=True)
        created_count = 0
        for user in users:
            UserProfile.objects.create(user=user)
            created_count = +1
            self.stdout.write(f'Created Profile for user: {user.username}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} user profiles'))