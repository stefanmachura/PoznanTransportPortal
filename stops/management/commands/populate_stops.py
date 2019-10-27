from django.core.management.base import BaseCommand, CommandError
from stops.models import Stop


class Command(BaseCommand):
    help = 'populates the stop db'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        Stop.objects.populate_db()
        self.stdout.write(self.style.SUCCESS('Stops database has been populated'))
