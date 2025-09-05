from django.core.management.base import BaseCommand
from AnalyticsApp.models import Product
import pandas as pd
from django.utils import timezone
from django.db import transaction


class Command(BaseCommand):
    help = 'Load dataset into the Product model'
    def add_arguments(self, parser):
        parser.add_argument('file_path', type= str, help='Path to the dataset file')

    def handle(self, *args, **options):
        # Logic to load dataset
        try:
            msg = 'Loading dataset...'
            data = pd.read_csv(options['file_path'])
            data_to_product = []
            self.stdout.write(self.style.NOTICE(msg))
            for _, row in data.iterrows():
                name = row.get('name', '')
                category = row['category']
                price = row['price']
                stock=row['stock'],
                created_at=row['created_at']
                if isinstance(created_at,str):
                    created_at = pd.to_datetime(created_at)
                if timezone.is_naive(created_at):
                    created_at = timezone.make_aware(created_at)

                if type(price) is str:
                    price = float(price)
                if type(stock) is str:
                    stock = int(stock)
        
                if not all([category, price, stock, created_at]):
                    continue
                data_to_product.append(Product(
                    name=row.get('name', ''),
                    category=row['category'],
                    price=row['price'],
                    stock=row['stock'],
                    created_at=row['created_at']
                ))

                with transaction.atomic():
                    Product.objects.bulk_create(data_to_product)
                    
            self.stdout.write(self.style.SUCCESS('Dataset loaded successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading dataset: {e}"))
        