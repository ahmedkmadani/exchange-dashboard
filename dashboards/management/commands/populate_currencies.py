from django.core.management.base import BaseCommand
from ...models import Currency


class Command(BaseCommand):
    help = 'Populate the Currency model with initial data'

    def handle(self, *args, **kwargs):
        currencies = [
            {'code': 'USD', 'name': 'US Dollar', 'symbol': '$'},
            {'code': 'SAR', 'name': 'Saudi Riyal', 'symbol': '﷼'},
            # Add more currencies as needed
        ]

        for currency in currencies:
            obj, created = Currency.objects.get_or_create(
                code=currency['code'],
                defaults={'name': currency['name'], 'symbol': currency['symbol']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added {currency['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"{currency['name']} already exists"))
