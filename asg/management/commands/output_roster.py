import csv
import sys
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from asg.models import *
from command_utils import get_ldap_info

class Command(BaseCommand):
    args = 'none'
    help = 'Outputs CSV data for all people in ASG'

    def handle(self, *args, **options):
        if 'output_dest' in options:
            # The value passed using output_dest might be a file 
            # or StringIO object
            writer = csv.writer(options['output_dest'])
        else:
            # Write results to stdout by default
            writer = csv.writer(sys.stdout)

        # Query: retrieve all people who are Senators/Exec members,
        # or who serve on a committee
        people = Person.objects.filter(Q(positions__isnull=False) |\
                                    Q(committee__isnull=False))\
                                    .distinct()\
                                    .order_by('last_name', 'first_name')

        # Write header row
        writer.writerow(('Name', 'Email', 'School', 'Position', 'Groups represented', 'Committee 1', 'Committee 2', 'Committee 3'))

        for person in people:
            # Some people haven't ever logged in, and if this is the case,
            # then person.user will be null. However, if they have,
            # we want to use their NetID since they might have changed
            # their email address.
            if person.user:
                info = get_ldap_info(netid=person.user.username)
            else:
                info = get_ldap_info(email=person.email)
            school = info['nuCurriculumOnly'][0]
            committees = person.committee_set.all()
            committee_1 = committees[0] if len(committees) > 0 else ''
            committee_2 = committees[1] if len(committees) > 1 else ''
            committee_3 = committees[2] if len(committees) > 2 else ''
            writer.writerow((person.full_name(), person.email, school, person.main_position(), person.groups_represented, committee_1, committee_2, committee_3))

