import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Product
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Populate database with new data after clearing old data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing old data...')
        self.clear_old_data()
        self.stdout.write('Old data cleared.')

        self.stdout.write('Populating database with new data...')
        self.populate_database()
        self.stdout.write('Database populated.')

    def clear_old_data(self):
        with transaction.atomic():
            Product.objects.all().delete()

    def populate_database(self):
        call_command('loaddata', 'products_fixture.json')
