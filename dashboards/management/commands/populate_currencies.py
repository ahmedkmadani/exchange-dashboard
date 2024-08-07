from django.core.management.base import BaseCommand
from ...models import Currency


class Command(BaseCommand):
    help = 'Populate the Currency model with initial data'

    def handle(self, *args, **kwargs):
        currencies = [
            {'code': 'USD', 'name': 'US Dollar', 'symbol': '$', 'flag_code': 'us'},
            {'code': 'SAR', 'name': 'Saudi Riyal', 'symbol': '﷼', 'flag_code': 'sa'},
            {'code': 'SDG', 'name': 'Sudanese Pound', 'symbol': 'جنيه', 'flag_code': 'sd'}
        ]

        for currency in currencies:
            obj, created = Currency.objects.get_or_create(
                code=currency['code'],
                defaults={
                    'name': currency['name'],
                    'symbol': currency['symbol'],
                    'flag_code': currency['flag_code'],  # Include the flag code here
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added {currency['name']}"))
            else:
                # Update the flag code if the currency already exists
                obj.flag_code = currency['flag_code']
                obj.save()
                self.stdout.write(self.style.WARNING(f"{currency['name']} already exists and flag code updated"))
