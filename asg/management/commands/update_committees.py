import csv
from django.core.management.base import BaseCommand, CommandError
from asg.models import *
from command_utils import get_ldap_info

class Command(BaseCommand):
    args = 'file.csv - a csv file (without headers) with two columns: Committee and personal Northwestern email address'
    help = 'Update current committee members based on a CSV file'

    def handle(self, *args, **options):
        pass
