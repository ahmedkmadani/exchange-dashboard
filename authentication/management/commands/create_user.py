from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create specified users if they do not already exist, or update them if they have changed.'

    def handle(self, *args, **kwargs):
        users_data = [
            {
                'password': '12570096',
                'first_name': 'Ali',
                'last_name': 'Hassan',
                'phone_number': 561363597
            }
        ]

        for user_data in users_data:
            phone_number = user_data['phone_number']
            password = user_data['password']
            first_name = user_data['first_name']
            last_name = user_data['last_name']

            # Check if the user already exists
            user, created = User.objects.get_or_create(
                username=phone_number,
                defaults={
                    'password': password,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'User "{phone_number}" created successfully.'))
            else:
                # Check if any details have changed
                updated = False
                if user.first_name != first_name or user.last_name != last_name or not user.check_password(password):
                    user.first_name = first_name
                    user.last_name = last_name
                    if not user.check_password(password):
                        user.set_password(password)
                    user.save()
                    updated = True

                if updated:
                    self.stdout.write(self.style.SUCCESS(f'User "{phone_number}" updated successfully.'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'User "{phone_number}" already exists and is up to date.'))
