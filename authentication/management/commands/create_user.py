from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a user with specified username and password if it does not already exist.'

    def handle(self, *args, **kwargs):
        password = 'alihassan'
        first_name = 'Ali'
        last_name = 'Hassan'
        phone_number = 123456789

        # Check if the user already exists
        if User.objects.filter(username=phone_number).exists():
            self.stdout.write(self.style.SUCCESS(f'User "{phone_number}" already exists.'))
        else:
            # Create the user
            User.objects.create_user(
                username=phone_number,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            self.stdout.write(self.style.SUCCESS(f'User "{phone_number}" created successfully.'))
