from django.core.management.base import BaseCommand, CommandError
from asg.models import Legislation

class Command(BaseCommand):
    args = 'none'
    help = 'Pull an updated list of legislation from the ASG website'

    def handle(self, *args, **options):
        pass
