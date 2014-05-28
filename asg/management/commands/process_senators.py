import re
from django.core.management.base import BaseCommand, CommandError
from asg.models import *

def substitute(contains, string):
    group = Person.objects.filter(groups_represented__contains=contains)
    for senator in group:
        senator.groups_represented = string
        senator.save()

paren_pat = re.compile(r'\((.*)\)')
def replace_from_parens(contains):
    group = Person.objects.filter(groups_represented__contains=contains)
    for senator in group:
        orig = senator.groups_represented
        match = paren_pat.search(orig)
        if match:
            senator.groups_represented = match.group(1)
            senator.save()

class Command(BaseCommand):
    args = 'None'
    help = 'Do some processing on Senators\' positions to make them human-readable'

    def handle(self, *args, **options):
        # Simple substitutions
        substitute('OFF', 'Off-Campus')
        substitute('IFC', 'Interfraternity Council')
        substitute('PHA', 'Panhellenic Association')

        # Use what's in the parenthesis
        replace_from_parens('RHA')
        replace_from_parens('RCB')
