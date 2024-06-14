from django.core.management import BaseCommand

from csv_reader.task import csv_analyze


class Command(BaseCommand):

    def handle(self, *args, **options):
        csv_analyze()
