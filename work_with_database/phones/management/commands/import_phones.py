import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import datetime
from phones.models import Phone

class Command(BaseCommand):
    help = 'Imports phones from a CSV file into the Phone model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the CSV file to be imported')

    def handle(self, *args, **options):
        csv_file_path = options['file_path']

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for row in reader:
                    try:
                        phone_obj, created = Phone.objects.update_or_create(
                            name=row['name'],
                            defaults={
                                'price': float(row['price']),
                                'image': row['image'],
                                'release_date': datetime.strptime(row['release_date'], '%Y-%m-%d').date(),
                                'lte_exists': row['lte_exists'].lower() == 'true',
                                'slug': slugify(row['name']),
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Successfully imported {phone_obj.name}'))
                        else:
                            self.stdout.write(self.style.SUCCESS(f'Updated {phone_obj.name}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error importing row with name "{row.get("name")}". Error: {e}'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{csv_file_path}" does not exist.'))
        except UnicodeDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Error decoding file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
