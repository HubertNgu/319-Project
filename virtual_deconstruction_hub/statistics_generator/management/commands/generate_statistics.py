from django.core.management.base import BaseCommand, CommandError
from statistics_generator import statistics

class Command(BaseCommand):
    args = ''
    help = 'Generates statistics based on data in the database'

    def handle(self, *args, **options):
        statistics.generate_statistics()
        self.stdout.write('Successfully generated statistics\n')
